from pydantic import BaseModel


class ProblemResponse(BaseModel):
    problem_id: int
    platform: str
    platform_problem_id: str
    title: str
    platform_difficulty: str | None
    cf_rating: int | None
    url: str
