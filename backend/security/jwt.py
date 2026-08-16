from datetime import datetime, timezone, timedelta
import os

import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
)

ACCESS_TOKEN_EXPIRE = timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)


def create_access_token(user_id: int) -> str:
    expiration = (
        datetime.now(timezone.utc)
        + ACCESS_TOKEN_EXPIRE
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token


def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError("Invalid token")

        return int(user_id)

    except (InvalidTokenError, ValueError):
        raise ValueError("Invalid token")
