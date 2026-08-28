import hashlib
import secrets


REFRESH_TOKEN_BYTES = 48


def create_refresh_token() -> tuple[str, str]:
    token = secrets.token_urlsafe(REFRESH_TOKEN_BYTES)
    token_hash = hash_refresh_token(token)

    return token, token_hash


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()
