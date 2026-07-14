from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from backend.models.user import User
from backend.models.problem import Problem
from backend.models.tag import Tag
from backend.models.problem_tag import ProblemTag
from backend.models.submission import Submission
from backend.models.contest_participation import ContestParticipation
from backend.models.user_session import UserSession
