from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.password_credential import PasswordCredential
from backend.security.password import hash_password
from backend.security.jwt import create_access_token
from backend.security.password import verify_password


class AuthService:

    def register(
        self,
        session: Session,
        username: str,
        email: str,
        password: str,
    ) -> User:

        existing_username = session.scalar(
            select(User).where(
                User.username == username
            )
        )

        if existing_username is not None:
            raise ValueError(
                "Username already exists."
            )

        existing_email = session.scalar(
            select(User).where(
                User.email == email
            )
        )

        if existing_email is not None:
            raise ValueError(
                "Email already exists."
            )

        user = User(
            username=username,
            email=email,
        )

        session.add(user)
        session.flush()

        password_credential = PasswordCredential(
            user_id=user.user_id,
            password_hash=hash_password(password),
        )

        session.add(password_credential)

        session.commit()
        session.refresh(user)

        return user

    def login(
        self,
        session: Session,
        email: str,
        password: str,
    ) -> str:

        user = session.scalar(
            select(User).where(
                User.email == email
            )
        )

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        credential = session.get(
            PasswordCredential,
            user.user_id,
        )

        if credential is None:
            raise ValueError(
                "Invalid email or password."
            )

        if not verify_password(
            password,
            credential.password_hash,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        return create_access_token(
            user.user_id
        )
