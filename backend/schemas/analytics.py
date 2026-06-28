from datetime import datetime

from pydantic import BaseModel


class UserSummaryResponse(
    BaseModel
):
    total_submissions: int
    accepted_submissions: int
    unique_solved_problems: int
    max_rating: int | None


class RatingHistoryEntry(
    BaseModel
):
    contest_name: str
    rating: int | None
    participated_at: datetime

class TopTagResponse(
    BaseModel
):
    tag: str
    solve_count: int

class VerdictBreakdownResponse(
    BaseModel
):
    verdict: str
    count: int

class TagSuccessRateResponse(
    BaseModel
):
    tag: str
    accepted_count: int
    failed_count: int
    success_rate: float

class RatingDistributionResponse(
    BaseModel
):
    rating: int
    solved: int

