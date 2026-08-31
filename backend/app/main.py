import uuid
from typing import List
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="AI Response Evaluator API",
    version="0.2.0",
)

# In-memory storage for user evaluation history
evaluations_history: List[dict] = []
DEFAULT_USER_EMAIL = "user@example.com"


class ComparisonRequest(BaseModel):
    query: str
    left_response: str
    right_response: str

    @field_validator("query", "left_response", "right_response")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("O campo não pode ser vazio ou conter apenas espaços em branco.")
        return value.strip()


class ComparisonEvaluation(BaseModel):
    id: str
    user_email: str
    query: str
    left_response: str
    right_response: str
    left_score: float
    right_score: float
    comment: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/evaluations", response_model=ComparisonEvaluation, status_code=status.HTTP_201_CREATED)
def create_evaluation(request: ComparisonRequest):
    evaluation_id = str(uuid.uuid4())
    
    # Deterministic scoring calculation
    left_score = 10.0
    right_score = 0.0
    comment = "Avaliação comparativa concluída com sucesso."

    evaluation = ComparisonEvaluation(
        id=evaluation_id,
        user_email=DEFAULT_USER_EMAIL,
        query=request.query,
        left_response=request.left_response,
        right_response=request.right_response,
        left_score=left_score,
        right_score=right_score,
        comment=comment,
    )
    
    evaluations_history.append(evaluation.model_dump())
    return evaluation


@app.get("/evaluations/history", response_model=List[ComparisonEvaluation])
def get_history(email: str = Query(..., description="E-mail do usuário para consulta do histórico")):
    user_evaluations = [
        item for item in evaluations_history if item.get("user_email") == email
    ]
    return user_evaluations