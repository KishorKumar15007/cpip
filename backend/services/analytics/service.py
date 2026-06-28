from fastapi import HTTPException, status

from backend.models.user import User

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models.submission import Submission
from backend.models.contest_participation import ContestParticipation
from backend.models.tag import Tag
from backend.models.problem import Problem
from backend.models.problem_tag import ProblemTag


class AnalyticsService:

    def _get_user(
        self,
        session: Session,
        user_id: int,
    ) -> User:
        user = session.get(
            User,
            user_id,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found.",
            )

        return user

    def get_user_summary(
        self,
        session: Session,
        user_id: int,
    ):
        self._get_user(
            session,
            user_id,
        )
        total_submissions = session.scalar(
            select(
                func.count()
            )
            .select_from(
                Submission
            )
            .where(
                Submission.user_id == user_id
            )
        )

        accepted_submissions = session.scalar(
            select(
                func.count()
            )
            .select_from(
                Submission
            )
            .where(
                Submission.user_id == user_id,
                Submission.verdict == "OK",
            )
        )

        unique_solved_problems = session.scalar(
            select(
                func.count(
                    func.distinct(
                        Submission.problem_id
                    )
                )
            )
            .where(
                Submission.user_id == user_id,
                Submission.verdict == "OK",
            )
        )

        max_rating = session.scalar(
            select(
                func.max(
                    ContestParticipation.new_rating
                )
            )
            .where(
                ContestParticipation.user_id
                == user_id
            )
        )

        return {
            "total_submissions":
                total_submissions,
            "accepted_submissions":
                accepted_submissions,
            "unique_solved_problems":
                unique_solved_problems,
            "max_rating":
                max_rating,
        }

    def get_rating_history(
        self,
        session: Session,
        user_id: int,
    ):
        self._get_user(
            session,
            user_id,
        )
        contests = session.scalars(
            select(
                ContestParticipation
            )
            .where(
                ContestParticipation.user_id
                == user_id
            )
            .order_by(
                ContestParticipation.participated_at
            )
        )

        return [
            {
                "contest_name":
                    contest.contest_name,
                "rating":
                    contest.new_rating,
                "participated_at":
                    contest.participated_at,
            }
            for contest in contests
        ]

    def get_top_tags(
        self,
        session: Session,
        user_id: int,
        limit: int = 10,
    ):
        self._get_user(
            session,
            user_id,
        )
        results = session.execute(
            select(
                Tag.name,
                func.count(
                    func.distinct(
                        Problem.problem_id
                    )
                ).label(
                    "solve_count"
                ),
            )
            .join(
                ProblemTag,
                Tag.tag_id
                == ProblemTag.tag_id,
            )
            .join(
                Problem,
                Problem.problem_id
                == ProblemTag.problem_id,
            )
            .join(
                Submission,
                Submission.problem_id
                == Problem.problem_id,
            )
            .where(
                Submission.user_id
                == user_id,
                Submission.verdict
                == "OK",
            )
            .group_by(
                Tag.name
            )
            .order_by(
                func.count(
                    func.distinct(
                        Problem.problem_id
                    )
                ).desc()
            )
            .limit(
                limit
            )
        )

        return [
            {
                "tag": tag,
                "solve_count": count,
            }
            for tag, count in results
        ]

    def get_verdict_breakdown(
        self,
        session: Session,
        user_id: int,
    ):
        self._get_user(
            session,
            user_id,
        )
        results = session.execute(
            select(
                Submission.verdict,
                func.count(),
            )
            .where(
                Submission.user_id == user_id
            )
            .group_by(
                Submission.verdict
            )
            .order_by(
                func.count().desc()
            )
        )

        return [
            {
                "verdict": verdict,
                "count": count,
            }
            for verdict, count in results
        ]

    def get_tag_success_rates(
        self,
        session: Session,
        user_id: int,
    ):
        self._get_user(
            session,
            user_id,
        )
        results = session.execute(
            select(
                Tag.name,

                func.count().filter(
                    Submission.verdict == "OK"
                ).label(
                    "accepted_count"
                ),

                func.count().filter(
                    Submission.verdict != "OK"
                ).label(
                    "failed_count"
                ),
            )
            .join(
                ProblemTag,
                Tag.tag_id
                == ProblemTag.tag_id,
            )
            .join(
                Problem,
                Problem.problem_id
                == ProblemTag.problem_id,
            )
            .join(
                Submission,
                Submission.problem_id
                == Problem.problem_id,
            )
            .where(
                Submission.user_id == user_id,
            )
            .group_by(
                Tag.name,
            )
        )

        tag_stats = []

        for (
            tag,
            accepted_count,
            failed_count,
        ) in results:

            total = (
                accepted_count
                + failed_count
            )

            success_rate = (
                accepted_count
                / total
                * 100
                if total > 0
                else 0
            )

            tag_stats.append(
                {
                    "tag": tag,
                    "accepted_count":
                        accepted_count,
                    "failed_count":
                        failed_count,
                    "success_rate":
                        round(
                            success_rate,
                            2,
                        ),
                }
            )

        return sorted(
            tag_stats,
            key=lambda row:
                row["success_rate"]
        )
    
    def get_rating_distribution(
        self,
        session: Session,
        user_id: int,
    ):
        self._get_user(
            session,
            user_id,
        )
        results = session.execute(
            select(
                Problem.cf_rating,
                func.count(
                    func.distinct(
                        Problem.problem_id
                    )
                ).label(
                    "solved_count"
                ),
            )
            .join(
                Submission,
                Submission.problem_id
                == Problem.problem_id,
            )
            .where(
                Submission.user_id == user_id,
                Submission.verdict == "OK",
                Problem.cf_rating.is_not(None),
            )
            .group_by(
                Problem.cf_rating,
            )
            .order_by(
                Problem.cf_rating,
            )
        )

        return [
            {
                "rating": rating,
                "solved": solved_count,
            }
            for rating, solved_count in results
        ]
