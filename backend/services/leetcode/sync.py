from sqlalchemy import select, func
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
        user = session.get(
            User,
            user_id,
        )

        if user is None:
            raise ValueError(
                f"User {user_id} not found."
            )

        if user.lc_username is None:
            raise ValueError(
                f"User {user_id} has no LeetCode username."
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
    
    def sync_problems(
        self,
        session: Session,
    ):
        problems_inserted = 0
        problems_skipped = 0
        tags_inserted = 0
        problem_tags_created = 0

        offset = 0
        limit = 100

        while True:

            result = self.client.get_problemset(
                offset=offset,
                limit=limit,
            )["problemsetQuestionListV2"]

            for raw_problem in result["questions"]:

                parsed_problem = parse_problem(
                    raw_problem,
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

                tags = parsed_problem.pop(
                    "tags"
                )

                problem = Problem(
                    **parsed_problem,
                )

                session.add(
                    problem,
                )

                problems_inserted += 1

                session.flush()

                for tag_name in tags:

                    tag = session.scalar(
                        select(Tag).where(
                            Tag.name == tag_name,
                        )
                    )

                    if tag is None:

                        tag = Tag(
                            name=tag_name,
                        )

                        session.add(
                            tag,
                        )

                        session.flush()

                        tags_inserted += 1

                    problem_tag = ProblemTag(
                        problem_id=problem.problem_id,
                        tag_id=tag.tag_id,
                    )

                    session.add(
                        problem_tag,
                    )

                    problem_tags_created += 1

            if not result["hasMore"]:
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

        if user.lc_username is None:
            raise ValueError(
                f"User {user_id} has no LeetCode username."
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
                    Submission.platform == "leetcode",
                )
            )
        }

        attempt_counts = {
            problem_id: attempts
            for problem_id, attempts in session.execute(
                select(
                    Submission.problem_id,
                    func.max(
                        Submission.attempt_number,
                    ),
                )
                .where(
                    Submission.user_id == user_id,
                    Submission.platform == "leetcode",
                )
                .group_by(
                    Submission.problem_id,
                )
            )
        }

        offset = 0
        limit = 100

        stop_sync = False

        while not stop_sync:

            result = self.client.get_submission_list(
                offset=offset,
                limit=limit,
            )["submissionList"]

            submissions = result["submissions"]

            for raw_submission in submissions:

                parsed_submission = parse_submission(
                    raw_submission,
                )

                if (
                    parsed_submission[
                        "platform_submission_id"
                    ]
                    in existing_submission_ids
                ):
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

                attempt_counts[problem_id] = (
                    attempt_counts.get(
                        problem_id,
                        0,
                    )
                    + 1
                )

                submission = Submission(
                    user_id=user_id,
                    session_id=None,
                    problem_id=problem_id,
                    attempt_number=attempt_counts[
                        problem_id
                    ],
                    **parsed_submission,
                )

                session.add(
                    submission,
                )

                existing_submission_ids.add(
                    parsed_submission[
                        "platform_submission_id"
                    ]
                )

                submissions_inserted += 1

            if (
                stop_sync
                or not result["hasNext"]
            ):
                break

            offset += limit

        session.commit()

        return {
            "submissions_inserted":
                submissions_inserted,
            "submissions_skipped":
                submissions_skipped,
            "missing_problems":
                missing_problems,
        }

    def sync_all(
        self,
        session: Session,
        user_id: int,
    ):
        return {
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
