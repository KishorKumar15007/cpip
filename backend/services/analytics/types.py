from datetime import datetime
from typing import TypedDict


class UserSummaryResult(TypedDict):
    total_submissions: int
    accepted_submissions: int
    unique_solved_problems: int
    max_rating: int | None


class RatingHistoryResult(TypedDict):
    contest_name: str
    rating: int | None
    participated_at: datetime


class TopTagResult(TypedDict):
    tag: str
    solve_count: int


class VerdictBreakdownResult(TypedDict):
    verdict: str
    count: int


class TagSuccessRateResult(TypedDict):
    tag: str
    accepted_count: int
    failed_count: int
    success_rate: float


class RatingDistributionResult(TypedDict):
    rating: int
    solved: int
