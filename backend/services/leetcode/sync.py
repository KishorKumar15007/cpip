from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.problem import Problem
from backend.models.tag import Tag
from backend.models.problem_tag import ProblemTag
from backend.models.submission import Submission
from backend.models.user_session import UserSession

from backend.services.leetcode.client import (
    LeetCodeClient,
)
from backend.services.leetcode.parsers import (
    parse_problem,
    parse_submission,
    parse_user,
)
from datetime import UTC, datetime, timedelta


SYNC_OVERLAP = timedelta(minutes=5)


class LeetCodeSyncService:

    def __init__(
        self,
        client: LeetCodeClient,
    ):
        self.client = client

    def sync_user(
        self,
        session: Session,
        user_id: int,
    ):
        try:
            user = session.get(
                User,
                user_id,
            )

            raw_user = self.client.get_user_profile(
                user.lc_username,
            )

            parsed_user = parse_user(
                raw_user,
            )

            user.lc_username = parsed_user[
                "lc_username"
            ]

            session.commit()

            return {
                "lc_username": user.lc_username,
            }

        except Exception:
            session.rollback()
            raise

    def sync_problems(
        self,
        session: Session,
    ):
        try:
            problems_inserted = 0
            problems_skipped = 0
            tags_inserted = 0
            problem_tags_created = 0

            offset = 0
            limit = 100

            while True:

                api_result = self.client.get_problemset(
                    offset=offset,
                    limit=limit,
                )["problemsetQuestionListV2"]

                for raw_problem in api_result["questions"]:

                    parsed_problem = parse_problem(
                        raw_problem,
                    )

                    tags = parsed_problem.pop(
                        "tags"
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

                if not api_result["hasMore"]:
                    break

                offset += limit

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

            if user.lc_last_synced_at is None:
                cutoff = None
            else:
                cutoff = (
                    user.lc_last_synced_at
                    - SYNC_OVERLAP
                )

            problem_map = {
                problem.url.removesuffix("/").split("/")[-1]:
                    problem.problem_id
                for problem in session.scalars(
                    select(Problem).where(
                        Problem.platform == "leetcode",
                    )
                )
            }

            existing_submission_ids = {
                submission_id
                for submission_id in session.scalars(
                    select(
                        Submission.platform_submission_id,
                    ).where(
                        Submission.user_id == user_id,
                        Submission.platform == "leetcode",
                    )
                )
            }

            offset = 0
            limit = 100
            stop_sync = False

            affected_problem_ids = set()

            while not stop_sync:

                api_result = self.client.get_submission_list(
                    offset=offset,
                    limit=limit,
                )["submissionList"]

                submissions = api_result["submissions"]

                if submissions is None:
                    return {
                        "status": "skipped",
                        "reason": (
                            "LeetCode submission history requires "
                            "an authenticated session."
                        ),
                    }

                for raw_submission in submissions:

                    submitted_at = datetime.fromtimestamp(
                        int(raw_submission["timestamp"]),
                        tz=UTC,
                    )

                    if (
                        cutoff is not None
                        and submitted_at < cutoff
                    ):
                        stop_sync = True
                        break

                    parsed_submission = parse_submission(
                        raw_submission,
                    )

                    submission_id = (
                        parsed_submission[
                            "platform_submission_id"
                        ]
                    )

                    if submission_id in existing_submission_ids:
                        submissions_skipped += 1
                        stop_sync = True
                        break

                    problem_slug = parsed_submission.pop(
                        "problem_slug"
                    )

                    problem_id = problem_map.get(
                        problem_slug,
                    )

                    if problem_id is None:
                        missing_problems += 1
                        continue

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
                        existing_submission_ids.add(
                            submission_id
                        )
                        affected_problem_ids.add(
                            problem_id
                        )
                        submissions_inserted += 1
                    else:
                        submissions_skipped += 1

                if (
                    stop_sync
                    or not api_result["hasNext"]
                ):
                    break

                offset += limit

            for problem_id in affected_problem_ids:

                ordered_submissions = session.scalars(
                    select(Submission)
                    .where(
                        Submission.user_id == user_id,
                        Submission.problem_id == problem_id,
                        Submission.platform == "leetcode",
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

        if not user.lc_username:
            return {
                "status": "skipped",
                "reason": "No LeetCode username.",
            }

        result = {
            "user": self.sync_user(
                session,
                user_id,
            ),
            "problems": self.sync_problems(
                session,
            ),
            "submissions": self.sync_submissions(
                session,
                user_id,
            ),
        }

        user.lc_last_synced_at = datetime.now(tz=UTC)
        
        session.commit()

        return result
