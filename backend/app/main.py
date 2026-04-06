from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.cases import get_case_by_id
from app.config import get_settings
from app.models import (
    CasesResponse,
    ErrorResponse,
    EvaluationRequest,
    EvaluationResponse,
    build_cases_response,
)
from app.services.evaluator import EvaluationServiceError, EvaluatorService


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="FastAPI backend for the AI Consulting Case Simulator MVP.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def get_evaluator() -> EvaluatorService:
    return EvaluatorService(settings=settings)


@app.get("/cases", response_model=CasesResponse)
def list_cases() -> CasesResponse:
    return build_cases_response()


@app.post(
    "/evaluate",
    response_model=EvaluationResponse,
    responses={400: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
)
def evaluate_case(payload: EvaluationRequest) -> EvaluationResponse:
    case = get_case_by_id(payload.case_id)
    if case is None:
        raise HTTPException(status_code=400, detail="Selected case does not exist.")

    try:
        result = get_evaluator().evaluate(case=case, response_text=payload.response)
    except EvaluationServiceError as exc:
        raise HTTPException(
            status_code=502,
            detail="Evaluation service is temporarily unavailable.",
        ) from exc

    return EvaluationResponse(case_id=payload.case_id, **result.model_dump())
