"""initial schema

Revision ID: 7f05d2d40075
Revises:
Create Date: 2026-07-14 17:23:19.023460

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7f05d2d40075"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "User",
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "username",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "lc_username",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "cf_username",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "last_synced_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint(
            "username",
            name="uq_user_username",
        ),
        sa.UniqueConstraint(
            "email",
            name="uq_user_email",
        ),
    )

    op.create_table(
        "Problems",
        sa.Column(
            "problem_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "platform",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "platform_problem_id",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "platform_difficulty",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "cf_rating",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "url",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("problem_id"),
        sa.UniqueConstraint(
            "platform",
            "platform_problem_id",
            name="uq_problems_platform_problem",
        ),
        sa.CheckConstraint(
            "platform IN ('codeforces', 'leetcode')",
            name="ck_problems_platform",
        ),
        sa.CheckConstraint(
            "cf_rating IS NULL OR cf_rating > 0",
            name="ck_problems_cf_rating",
        ),
    )

    op.create_table(
        "Tags",
        sa.Column(
            "tag_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.Text(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("tag_id"),
        sa.UniqueConstraint(
            "name",
            name="uq_tags_name",
        ),
    )

    op.create_table(
        "ProblemTags",
        sa.Column(
            "problem_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "tag_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["Problems.problem_id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["Tags.tag_id"],
        ),
        sa.PrimaryKeyConstraint(
            "problem_id",
            "tag_id",
        ),
    )

    op.create_table(
        "UserSessions",
        sa.Column(
            "session_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "ended_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["User.user_id"],
        ),
        sa.PrimaryKeyConstraint("session_id"),
        sa.CheckConstraint(
            "ended_at > started_at",
            name="ck_usersessions_time",
        ),
    )

    op.create_table(
        "ContestParticipation",
        sa.Column(
            "participation_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "platform",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "contest_id",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "contest_name",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "rank",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "old_rating",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "new_rating",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "participated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["User.user_id"],
        ),
        sa.PrimaryKeyConstraint("participation_id"),
        sa.UniqueConstraint(
            "user_id",
            "platform",
            "contest_id",
            name="uq_contestparticipation_user_platform_contest",
        ),
    )

    op.create_table(
        "Submissions",
        sa.Column(
            "submission_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            sa.BigInteger(),
            nullable=True,
        ),
        sa.Column(
            "problem_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "platform",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "platform_submission_id",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "verdict",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "language",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "attempt_number",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["Problems.problem_id"],
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["UserSessions.session_id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["User.user_id"],
        ),
        sa.PrimaryKeyConstraint("submission_id"),
        sa.UniqueConstraint(
            "platform",
            "platform_submission_id",
            name="uq_submissions_platform_submission",
        ),
        sa.CheckConstraint(
            "attempt_number > 0",
            name="ck_submissions_attempt_number",
        ),
    )

    op.create_index(
        "idx_usersessions_user_id",
        "UserSessions",
        ["user_id"],
    )

    op.create_index(
        "idx_submissions_user_id",
        "Submissions",
        ["user_id"],
    )

    op.create_index(
        "idx_submissions_problem_id",
        "Submissions",
        ["problem_id"],
    )

    op.create_index(
        "idx_submissions_session_id",
        "Submissions",
        ["session_id"],
    )

    op.create_index(
        "idx_submissions_submitted_at",
        "Submissions",
        ["submitted_at"],
    )

    op.create_index(
        "idx_submissions_user_problem",
        "Submissions",
        ["user_id", "problem_id"],
    )

    op.create_index(
        "idx_contestparticipation_user_id",
        "ContestParticipation",
        ["user_id"],
    )

    op.create_index(
        "idx_contestparticipation_user_date",
        "ContestParticipation",
        ["user_id", "participated_at"],
    )

    op.create_index(
        "idx_problemtags_problem_id",
        "ProblemTags",
        ["problem_id"],
    )

    op.create_index(
        "idx_problemtags_tag_id",
        "ProblemTags",
        ["tag_id"],
    )

    op.create_index(
        "idx_problems_platform",
        "Problems",
        ["platform"],
    )


def downgrade() -> None:
    op.drop_table("Submissions")
    op.drop_table("ContestParticipation")
    op.drop_table("UserSessions")
    op.drop_table("ProblemTags")
    op.drop_table("Tags")
    op.drop_table("Problems")
    op.drop_table("User")
