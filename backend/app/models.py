from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.cases import CASE_DEFINITIONS
from app.config import get_settings


CaseId = Literal["profitability", "market_entry", "m_and_a"]


class CaseSummary(BaseModel):
    id: CaseId
    title: str
    prompt: str


class CasesResponse(BaseModel):
    cases: list[CaseSummary]


class EvaluationRequest(BaseModel):
    case_id: CaseId = Field(description="The selected case identifier.")
    response: str = Field(description="The user's written case response.")

    @field_validator("response")
    @classmethod
    def validate_response_length(cls, value: str) -> str:
        trimmed = value.strip()
        settings = get_settings()
        if not trimmed:
            raise ValueError("Response cannot be empty.")
        if len(trimmed) < settings.min_response_length:
            raise ValueError(
                f"Response must be at least {settings.min_response_length} characters."
            )
        if len(trimmed) > settings.max_response_length:
            raise ValueError(
                f"Response must be at most {settings.max_response_length} characters."
            )
        return trimmed


class EvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: int = Field(ge=0, le=100)
    strengths: list[str] = Field(min_length=1, max_length=4)
    weaknesses: list[str] = Field(min_length=1, max_length=4)
    recommendations: list[str] = Field(min_length=1, max_length=4)


class EvaluationResponse(EvaluationResult):
    case_id: CaseId


class ErrorResponse(BaseModel):
    detail: str


def build_cases_response() -> CasesResponse:
    return CasesResponse(
        cases=[
            CaseSummary(id=case.id, title=case.title, prompt=case.prompt)
            for case in CASE_DEFINITIONS
        ]
    )
