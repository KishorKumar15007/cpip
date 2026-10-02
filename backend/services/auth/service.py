from datetime import datetime, timedelta, timezone
import json
import os
import secrets

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import IntegrityError
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
from backend.redis_client import redis_client


load_dotenv()


REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.environ["REFRESH_TOKEN_EXPIRE_DAYS"]
)
REGISTRATION_STATE_SECONDS = 10 * 60


class AuthService:

    def issue_session(self, session: Session, user_id: int) -> tuple[str, str]:
        access_token = create_access_token(user_id)
        refresh_token, refresh_token_hash = create_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        session.add(RefreshToken(user_id=user_id, token_hash=refresh_token_hash, expires_at=expires_at))
        try:
            session.commit()
        except IntegrityError as error:
            session.rollback()
            if "username" in str(error).lower():
                raise ValueError("Username unavailable.") from error
            raise
        return access_token, refresh_token

    def begin_registration(
        self,
        session: Session,
        email: str,
        password: str,
    ) -> str:
        existing_email = session.scalar(
            select(User).where(
                User.email == email
            )
        )

        if existing_email is not None:
            raise ValueError(
                "Email already exists."
            )

        registration_id = secrets.token_urlsafe(32)
        redis_client.set(
            f"auth:registration:{registration_id}",
            json.dumps({"email": email, "password_hash": hash_password(password)}),
            ex=REGISTRATION_STATE_SECONDS,
        )
        return registration_id

    def finalize_registration(self, session: Session, registration_id: str, username: str) -> tuple[User, str, str]:
        normalized = username.strip()
        if not normalized or len(normalized) > 80:
            raise ValueError("Username must be between 1 and 80 characters.")
        state_key = f"auth:registration:{registration_id}"
        raw_state = redis_client.get(state_key)
        if raw_state is None:
            raise ValueError("Registration session expired. Start again.")
        state = json.loads(raw_state)
        existing_email = session.scalar(select(User).where(User.email == state["email"]))
        if existing_email is not None:
            raise ValueError("Email already exists.")
        existing = session.scalar(select(User).where(User.username == normalized))
        if existing is not None:
            raise ValueError("Username unavailable.")
        user = User(email=state["email"], username=normalized)
        session.add(user)
        session.flush()
        session.add(PasswordCredential(user_id=user.user_id, password_hash=state["password_hash"]))
        try:
            session.commit()
        except IntegrityError as error:
            session.rollback()
            if "username" in str(error).lower():
                raise ValueError("Username unavailable.") from error
            raise
        session.refresh(user)
        redis_client.delete(state_key)
        access_token, refresh_token = self.issue_session(session, user.user_id)
        return user, access_token, refresh_token

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

        return self.issue_session(session, user.user_id)

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

        try:
            session.commit()
        except IntegrityError as error:
            session.rollback()
            if "username" in str(error).lower():
                raise ValueError("Username unavailable.") from error
            raise

        return access_token, new_refresh_token

    def revoke_refresh_token(self, session: Session, refresh_token: str) -> None:
        stored_token = session.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_refresh_token(refresh_token)))
        if stored_token is not None:
            stored_token.revoked_at = datetime.now(timezone.utc)
            session.commit()
