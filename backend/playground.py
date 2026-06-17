''' FOR TESTING PURPOSES ONLY'''


import time

from sqlalchemy import func, select

from backend.db.session import SessionLocal

from backend.models.problem import Problem
from backend.models.tag import Tag
from backend.models.problem_tag import ProblemTag
from backend.models.contest_participation import (
    ContestParticipation,
)
from backend.models.submission import Submission


start = time.perf_counter()

with SessionLocal() as session:

    problems = session.scalar(
        select(func.count())
        .select_from(Problem)
    )

    tags = session.scalar(
        select(func.count())
        .select_from(Tag)
    )

    problem_tags = session.scalar(
        select(func.count())
        .select_from(ProblemTag)
    )

    contests = session.scalar(
        select(func.count())
        .select_from(ContestParticipation)
    )

    submissions = session.scalar(
        select(func.count())
        .select_from(Submission)
    )

print(f"Problems: {problems}")
print(f"Tags: {tags}")
print(f"ProblemTags: {problem_tags}")
print(f"ContestParticipation: {contests}")
print(f"Submissions: {submissions}")

end = time.perf_counter()

print(
    f"Verification completed in {end - start:.2f} seconds"
)
