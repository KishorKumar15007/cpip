from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api.dependencies import get_session
from backend.models.problem import Problem
from backend.schemas.problem import ProblemResponse


router = APIRouter(
    prefix="/problems",
    tags=["Problems"],
)


@router.get(
    "",
    response_model=list[ProblemResponse],
)
def get_problems(
    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        0,
        ge=0,
    ),
    session: Session = Depends(get_session),
):
    problems = session.scalars(
        select(Problem)
        .order_by(Problem.problem_id)
        .limit(limit)
        .offset(offset)
    ).all()

    return problems
