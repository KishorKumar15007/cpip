from datetime import datetime

from pydantic import BaseModel


class SubmissionResponse(BaseModel):
    submission_id: int
    problem_id: int
    platform: str
    platform_submission_id: str
    verdict: str
    language: str
    submitted_at: datetime
    attempt_number: int
