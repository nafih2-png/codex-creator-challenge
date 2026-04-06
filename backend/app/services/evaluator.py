import json
from statistics import mean

from openai import APIError, APITimeoutError, OpenAI

from app.cases import CaseDefinition
from app.config import Settings
from app.models import EvaluationResult


class EvaluationServiceError(Exception):
    """Raised when evaluation cannot be completed."""


class EvaluatorService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.request_timeout_seconds,
        ) if settings.openai_api_key else None

    def evaluate(self, case: CaseDefinition, response_text: str) -> EvaluationResult:
        if self.client is None:
            return self._evaluate_locally(case=case, response_text=response_text)

        try:
            response = self.client.responses.create(
                model=self.settings.openai_model,
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are evaluating a consulting case interview response. "
                            "Return JSON only. Score the response using four dimensions: "
                            "structure, logic, clarity, and business judgment."
                        ),
                    },
                    {
                        "role": "user",
                        "content": self._build_user_prompt(
                            case=case,
                            response_text=response_text,
                        ),
                    },
                ],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "case_evaluation",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "score": {"type": "integer"},
                                "strengths": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "weaknesses": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "recommendations": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                            },
                            "required": [
                                "score",
                                "strengths",
                                "weaknesses",
                                "recommendations",
                            ],
                            "additionalProperties": False,
                        },
                    }
                },
                max_output_tokens=350,
            )
        except (APIError, APITimeoutError) as exc:
            raise EvaluationServiceError("OpenAI evaluation failed.") from exc

        try:
            parsed = json.loads(response.output_text)
            return EvaluationResult.model_validate(parsed)
        except (json.JSONDecodeError, ValueError) as exc:
            raise EvaluationServiceError("Evaluation response could not be parsed.") from exc

    def _build_user_prompt(self, case: CaseDefinition, response_text: str) -> str:
        return (
            f"Case type: {case.id}\n"
            f"Case title: {case.title}\n"
            f"Case prompt: {case.prompt}\n\n"
            "Evaluate the candidate's written answer using this rubric:\n"
            "- structure: Is the response organized and MECE-like?\n"
            "- logic: Does the reasoning connect evidence to conclusions?\n"
            "- clarity: Is the communication concise and easy to follow?\n"
            "- business judgment: Are the recommendations practical and commercially sound?\n\n"
            "Return JSON with:\n"
            "- score: integer from 0 to 100\n"
            "- strengths: 1 to 4 bullet-like strings\n"
            "- weaknesses: 1 to 4 bullet-like strings\n"
            "- recommendations: 1 to 4 bullet-like strings\n\n"
            f"Candidate response:\n{response_text}"
        )

    def _evaluate_locally(
        self,
        case: CaseDefinition,
        response_text: str,
    ) -> EvaluationResult:
        lowered = response_text.lower()
        paragraphs = [part.strip() for part in response_text.split("\n") if part.strip()]
        word_count = len(response_text.split())

        structure_score = 50
        if len(paragraphs) >= 2:
            structure_score += 15
        if any(marker in lowered for marker in ("first", "second", "finally", "1.", "2.")):
            structure_score += 20
        if any(marker in lowered for marker in ("framework", "bucket", "drivers")):
            structure_score += 10
        structure_score = min(structure_score, 95)

        logic_score = 50
        if any(marker in lowered for marker in ("because", "therefore", "if", "then")):
            logic_score += 20
        if any(marker in lowered for marker in ("data", "cost", "revenue", "market", "customer")):
            logic_score += 15
        if word_count >= 120:
            logic_score += 10
        logic_score = min(logic_score, 95)

        clarity_score = 55
        if 100 <= word_count <= 320:
            clarity_score += 20
        if len(paragraphs) >= 2:
            clarity_score += 10
        if len(response_text.split(".")) >= 3:
            clarity_score += 10
        clarity_score = min(clarity_score, 95)

        business_score = 50
        case_keywords = {
            "profitability": ("cost", "pricing", "route", "operations", "margin"),
            "market_entry": ("competition", "consumer", "regulation", "partner", "channel"),
            "m_and_a": ("synergy", "integration", "valuation", "risk", "capability"),
        }
        matches = sum(1 for keyword in case_keywords[case.id] if keyword in lowered)
        business_score += min(matches * 10, 30)
        if any(marker in lowered for marker in ("recommend", "prioritize", "risk", "next step")):
            business_score += 10
        business_score = min(business_score, 95)

        overall = round(mean([structure_score, logic_score, clarity_score, business_score]))
        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[str] = []

        if structure_score >= 70:
            strengths.append("Your answer has a visible structure rather than a stream of ideas.")
        else:
            weaknesses.append("The response needs a clearer top-down structure and issue tree.")
            recommendations.append("Open with a 2 to 3-part framework before diving into analysis.")

        if logic_score >= 70:
            strengths.append("You connect points with reasoning instead of listing observations only.")
        else:
            weaknesses.append("Some conclusions are not fully supported by explicit reasoning.")
            recommendations.append("Use cause-and-effect language to link facts, assumptions, and conclusions.")

        if clarity_score >= 70:
            strengths.append("The response is readable and mostly easy to follow.")
        else:
            weaknesses.append("The communication could be more concise and easier to scan.")
            recommendations.append("Break the answer into short paragraphs or numbered points.")

        if business_score >= 70:
            strengths.append("Your recommendation shows practical business awareness.")
        else:
            weaknesses.append("The business recommendation needs stronger commercial judgment.")
            recommendations.append("State the key decision, major risks, and one practical next step.")

        if not strengths:
            strengths.append("You addressed the case prompt directly, which is a solid starting point.")
        if not weaknesses:
            weaknesses.append("The answer could still be sharper by making tradeoffs more explicit.")
        if not recommendations:
            recommendations.append(
                "Quantify the biggest driver and make the recommendation more decisive."
            )

        return EvaluationResult(
            score=max(0, min(overall, 100)),
            strengths=strengths[:4],
            weaknesses=weaknesses[:4],
            recommendations=recommendations[:4],
        )
