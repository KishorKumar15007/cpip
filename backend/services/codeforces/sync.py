from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.problem import Problem
from backend.models.problem_tag import ProblemTag
from backend.models.tag import Tag
from backend.models.submission import Submission
from backend.models.contest_participation import ContestParticipation
from backend.models.user_session import UserSession # For SQLAlchemy FK Resolution

from backend.services.codeforces.client import (
    CodeforcesClient,
)
from backend.services.codeforces.parsers import (
    parse_problem,
    parse_tags,
    parse_contest_participation,
    parse_submission,
)


class CodeforcesSyncService:

    def __init__(
        self,
        client: CodeforcesClient,
    ):
        self.client = client

    def sync_problems(
        self,
        session: Session,
    ):
        problems_inserted = 0
        problems_skipped = 0
        tags_inserted = 0
        problem_tags_created = 0

        result = self.client.get_problemset()

        problems = result["problems"]

        for raw_problem in problems:

            parsed_problem = parse_problem(
                raw_problem
            )

            existing_problem = session.scalar(
                select(Problem).where(
                    Problem.platform
                    == parsed_problem["platform"],
                    Problem.platform_problem_id
                    == parsed_problem[
                        "platform_problem_id"
                    ],
                )
            )

            if existing_problem:
                problems_skipped += 1
                continue

            problem = Problem(
                **parsed_problem
            )

            session.add(problem)

            problems_inserted += 1

            session.flush()

            tags = parse_tags(raw_problem)

            for tag_name in tags:

                tag = session.scalar(
                    select(Tag).where(
                        Tag.name == tag_name
                    )
                )

                if tag is None:

                    tag = Tag(
                        name=tag_name
                    )

                    session.add(tag)

                    tags_inserted += 1

                    session.flush()

                problem_tag = ProblemTag(
                    problem_id=problem.problem_id,
                    tag_id=tag.tag_id,
                )

                session.add(problem_tag)

                problem_tags_created += 1

        session.commit()

        return {
            "problems_inserted": problems_inserted,
            "problems_skipped": problems_skipped,
            "tags_inserted": tags_inserted,
            "problem_tags_created": problem_tags_created,
        }

    def sync_contest_history(
        self,
        session: Session,
        user_id: int,
    ):
        contests_inserted = 0
        contests_skipped = 0

        user = session.get(
            User,
            user_id,
        )

        if user is None:
            raise ValueError(
                f"User {user_id} not found."
            )

        if user.cf_username is None:
            raise ValueError(
                f"User {user_id} has no Codeforces handle."
            )

        contests = self.client.get_user_rating(
            user.cf_username
        )

        for raw_contest in contests:

            parsed_contest = (
                parse_contest_participation(
                    raw_contest
                )
            )

            existing_contest = session.scalar(
                select(ContestParticipation).where(
                    ContestParticipation.user_id
                    == user_id,
                    ContestParticipation.platform
                    == parsed_contest["platform"],
                    ContestParticipation.contest_id
                    == parsed_contest["contest_id"],
                )
            )

            if existing_contest:
                contests_skipped += 1
                continue

            contest = ContestParticipation(
                user_id=user_id,
                **parsed_contest,
            )

            session.add(contest)

            contests_inserted += 1

        session.commit()

        return {
            "contests_inserted": contests_inserted,
            "contests_skipped": contests_skipped,
        }

    def sync_submissions(
        self,
        session: Session,
        user_id: int,
    ):
        submissions_inserted = 0
        submissions_skipped = 0
        missing_problems = 0

        user = session.get(
            User,
            user_id,
        )

        if user is None:
            raise ValueError(
                f"User {user_id} not found."
            )

        if user.cf_username is None:
            raise ValueError(
                f"User {user_id} has no Codeforces handle."
            )

        submissions = self.client.get_user_submissions(
            user.cf_username
        )

        submissions.sort(
            key=lambda s: s["creationTimeSeconds"]
        )

        problem_map = {
            (
                problem.platform,
                problem.platform_problem_id,
            ): problem.problem_id
            for problem in session.scalars(
                select(Problem)
            )
        }

        existing_submission_ids = {
            submission.platform_submission_id
            for submission in session.scalars(
                select(Submission)
            )
        }

        attempt_counts = {}

        for raw_submission in submissions:

            parsed_submission = parse_submission(
                raw_submission
            )

            if (
                parsed_submission[
                    "platform_submission_id"
                ]
                in existing_submission_ids
            ):
                submissions_skipped += 1
                continue

            contest_id = (
                raw_submission["problem"]
                .get("contestId")
            )

            index = (
                raw_submission["problem"]
                .get("index")
            )

            if (
                contest_id is None
                or index is None
            ):
                missing_problems += 1
                continue

            platform_problem_id = (
                f"{contest_id}{index}"
            )

            problem_id = problem_map.get(
                (
                    "codeforces",
                    platform_problem_id,
                )
            )

            if problem_id is None:
                missing_problems += 1
                continue

            key = (
                user_id,
                problem_id,
            )

            attempt_counts[key] = (
                attempt_counts.get(key, 0)
                + 1
            )

            submission = Submission(
                user_id=user_id,
                session_id=None,
                problem_id=problem_id,
                attempt_number=attempt_counts[
                    key
                ],
                **parsed_submission,
            )

            session.add(submission)

            submissions_inserted += 1

        session.commit()

        return {
            "submissions_inserted": (
                submissions_inserted
            ),
            "submissions_skipped": (
                submissions_skipped
            ),
            "missing_problems": (
                missing_problems
            ),
        }

    def sync_all(
        self,
        session: Session,
        user_id: int,
    ):
        return {
            "problems": self.sync_problems(
                session,
            ),
            "contests": self.sync_contest_history(
                session,
                user_id,
            ),
            "submissions": self.sync_submissions(
                session,
                user_id,
            ),
        }
