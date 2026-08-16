from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_user, get_session
from backend.models.submission import Submission
from backend.models.user import User
from backend.schemas.submission import SubmissionResponse


router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.get(
    "",
    response_model=list[SubmissionResponse],
)
def get_submissions(
    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        0,
        ge=0,
    ),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    submissions = session.scalars(
        select(Submission)
        .where(
            Submission.user_id == current_user.user_id,
        )
        .order_by(
            Submission.submitted_at.desc(),
            Submission.submission_id.desc(),
        )
        .limit(limit)
        .offset(offset)
    ).all()

    return submissions
