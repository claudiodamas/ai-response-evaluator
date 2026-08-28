import uuid
from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI Response Evaluator API",
    version="0.1.0",
)


# In-memory database simulation
evaluations_db = {}


class EvaluationCreate(BaseModel):
    prompt: str
    response: str
    score: float = Field(ge=0, le=10)
    feedback: str


class Evaluation(EvaluationCreate):
    id: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/evaluations", response_model=Evaluation, status_code=status.HTTP_201_CREATED)
def create_evaluation(evaluation_in: EvaluationCreate):
    evaluation_id = str(uuid.uuid4())
    evaluation = Evaluation(
        id=evaluation_id,
        prompt=evaluation_in.prompt,
        response=evaluation_in.response,
        score=evaluation_in.score,
        feedback=evaluation_in.feedback,
    )
    evaluations_db[evaluation_id] = evaluation
    return evaluation


@app.get("/evaluations", response_model=List[Evaluation])
def list_evaluations():
    return list(evaluations_db.values())


@app.get("/evaluations/{evaluation_id}", response_model=Evaluation)
def get_evaluation(evaluation_id: str):
    if evaluation_id not in evaluations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluation not found",
        )
    return evaluations_db[evaluation_id]