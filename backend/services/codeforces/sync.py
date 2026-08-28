from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.problem import Problem
from backend.models.problem_tag import ProblemTag
from backend.models.tag import Tag
from backend.models.submission import Submission
from backend.models.contest_participation import ContestParticipation
from backend.models.user_session import UserSession

from backend.services.codeforces.client import (
    CodeforcesClient,
)
from backend.services.codeforces.parsers import (
    parse_problem,
    parse_tags,
    parse_contest_participation,
    parse_submission,
)
from datetime import UTC, datetime, timedelta


SYNC_OVERLAP = timedelta(minutes=5)


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
        try:
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

                stmt = (
                    insert(Problem)
                    .values(**parsed_problem)
                    .on_conflict_do_nothing(
                        index_elements=[
                            "platform",
                            "platform_problem_id",
                        ],
                    )
                    .returning(Problem.problem_id)
                )

                problem_id = session.scalar(stmt)

                if problem_id is None:
                    problems_skipped += 1
                    continue

                problems_inserted += 1

                tags = parse_tags(raw_problem)

                for tag_name in tags:

                    stmt = (
                        insert(Tag)
                        .values(
                            name=tag_name,
                        )
                        .on_conflict_do_nothing(
                            index_elements=["name"],
                        )
                        .returning(Tag.tag_id)
                    )

                    tag_id = session.scalar(stmt)

                    if tag_id is None:
                        tag_id = session.scalar(
                            select(Tag.tag_id).where(
                                Tag.name == tag_name,
                            )
                        )
                    else:
                        tags_inserted += 1

                    stmt = (
                        insert(ProblemTag)
                        .values(
                            problem_id=problem_id,
                            tag_id=tag_id,
                        )
                        .on_conflict_do_nothing()
                    )

                    insert_result = session.execute(stmt)

                    if insert_result.rowcount:
                        problem_tags_created += 1

            session.commit()

            return {
                "problems_inserted":
                    problems_inserted,
                "problems_skipped":
                    problems_skipped,
                "tags_inserted":
                    tags_inserted,
                "problem_tags_created":
                    problem_tags_created,
            }

        except Exception:
            session.rollback()
            raise

    def sync_contest_history(
        self,
        session: Session,
        user_id: int,
    ):
        try:
            contests_inserted = 0
            contests_skipped = 0

            user = session.get(
                User,
                user_id,
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

                stmt = (
                    insert(ContestParticipation)
                    .values(
                        user_id=user_id,
                        **parsed_contest,
                    )
                    .on_conflict_do_nothing(
                        index_elements=[
                            "user_id",
                            "platform",
                            "contest_id",
                        ],
                    )
                )

                insert_result = session.execute(stmt)

                if insert_result.rowcount:
                    contests_inserted += 1
                else:
                    contests_skipped += 1

            session.commit()

            return {
                "contests_inserted":
                    contests_inserted,
                "contests_skipped":
                    contests_skipped,
            }

        except Exception:
            session.rollback()
            raise

    def sync_submissions(
        self,
        session: Session,
        user_id: int,
    ):
        try:
            submissions_inserted = 0
            submissions_skipped = 0
            missing_problems = 0

            user = session.get(
                User,
                user_id,
            )

            if user.cf_last_synced_at is None:
                cutoff = None
            else:
                cutoff = (
                    user.cf_last_synced_at
                    - SYNC_OVERLAP
                )

            submissions = self.client.get_user_submissions(
                user.cf_username
            )

            submissions.sort(
                key=lambda s: (
                    s["creationTimeSeconds"],
                    s["id"],
                ),
                reverse=True,
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
                    select(Submission).where(
                        Submission.user_id == user_id,
                        Submission.platform == "codeforces",
                    )
                )
            }

            new_submissions = []

            for raw_submission in submissions:

                submitted_at = datetime.fromtimestamp(
                    raw_submission[
                        "creationTimeSeconds"
                    ],
                    tz=UTC,
                )

                if (
                    cutoff is not None
                    and submitted_at < cutoff
                ):
                    break

                parsed_submission = parse_submission(
                    raw_submission
                )

                submission_id = (
                    parsed_submission[
                        "platform_submission_id"
                    ]
                )

                if submission_id in existing_submission_ids:
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

                new_submissions.append(
                    (
                        raw_submission,
                        parsed_submission,
                        problem_id,
                    )
                )

            new_submissions.sort(
                key=lambda item: (
                    item[0]["creationTimeSeconds"],
                    item[0]["id"],
                )
            )

            for (
                raw_submission,
                parsed_submission,
                problem_id,
            ) in new_submissions:

                stmt = (
                    insert(Submission)
                    .values(
                        user_id=user_id,
                        session_id=None,
                        problem_id=problem_id,
                        attempt_number=0,
                        **parsed_submission,
                    )
                    .on_conflict_do_nothing(
                        index_elements=[
                            "platform",
                            "platform_submission_id",
                        ],
                    )
                )

                insert_result = session.execute(stmt)

                if insert_result.rowcount:
                    submissions_inserted += 1
                    existing_submission_ids.add(
                        parsed_submission[
                            "platform_submission_id"
                        ]
                    )
                else:
                    submissions_skipped += 1

            problem_ids = {
                problem_id
                for (
                    _,
                    _,
                    problem_id,
                ) in new_submissions
            }

            for problem_id in problem_ids:

                ordered_submissions = session.scalars(
                    select(Submission)
                    .where(
                        Submission.user_id == user_id,
                        Submission.problem_id == problem_id,
                        Submission.platform == "codeforces",
                    )
                    .order_by(
                        Submission.submitted_at.asc(),
                        Submission.platform_submission_id.asc(),
                    )
                ).all()

                for attempt_number, submission in enumerate(
                    ordered_submissions,
                    start=1,
                ):
                    submission.attempt_number = (
                        attempt_number
                    )

            session.commit()

            return {
                "submissions_inserted":
                    submissions_inserted,
                "submissions_skipped":
                    submissions_skipped,
                "missing_problems":
                    missing_problems,
            }

        except Exception:
            session.rollback()
            raise

    def sync_all(
        self,
        session: Session,
        user_id: int,
    ):
        user = session.get(
            User,
            user_id,
        )

        if user is None:
            raise ValueError(
                f"User {user_id} not found."
            )

        if not user.cf_username:
            return {
                "status": "skipped",
                "reason": "No Codeforces handle.",
            }

        result = {
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

        user.cf_last_synced_at = datetime.now(
            tz=UTC
        )

        session.commit()

        return result
