from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.password_credential import PasswordCredential
from backend.models.refresh_token import RefreshToken
from backend.security.jwt import create_access_token
from backend.security.password import hash_password, verify_password
from backend.security.refresh_token import (
    create_refresh_token,
    hash_refresh_token,
)


load_dotenv()


REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.environ["REFRESH_TOKEN_EXPIRE_DAYS"]
)


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
    ) -> tuple[str, str]:

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

        access_token = create_access_token(
            user.user_id
        )

        refresh_token, refresh_token_hash = (
            create_refresh_token()
        )

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        session.add(
            RefreshToken(
                user_id=user.user_id,
                token_hash=refresh_token_hash,
                expires_at=expires_at,
            )
        )

        session.commit()

        return access_token, refresh_token

    def refresh(
        self,
        session: Session,
        refresh_token: str,
    ) -> tuple[str, str]:

        token_hash = hash_refresh_token(
            refresh_token
        )

        stored_token = session.scalar(
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash
            )
            .with_for_update()
        )

        now = datetime.now(timezone.utc)

        if (
            stored_token is None
            or stored_token.revoked_at is not None
            or stored_token.expires_at <= now
        ):
            raise ValueError(
                "Invalid or expired refresh token."
            )

        user = session.get(
            User,
            stored_token.user_id,
        )

        if user is None:
            raise ValueError(
                "Invalid or expired refresh token."
            )

        stored_token.revoked_at = now

        new_refresh_token, new_refresh_token_hash = (
            create_refresh_token()
        )

        new_expires_at = (
            now
            + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        session.add(
            RefreshToken(
                user_id=user.user_id,
                token_hash=new_refresh_token_hash,
                expires_at=new_expires_at,
            )
        )

        access_token = create_access_token(
            user.user_id
        )

        session.commit()

        return access_token, new_refresh_token
