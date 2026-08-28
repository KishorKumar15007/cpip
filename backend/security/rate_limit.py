import os

from dotenv import load_dotenv
from redis import Redis


load_dotenv()


REDIS_URL = os.environ["REDIS_URL"]

LOGIN_RATE_LIMIT = 5
LOGIN_RATE_WINDOW_SECONDS = 60


redis_client = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


def check_login_rate_limit(
    client_ip: str,
) -> int | None:
    key = f"rate_limit:login:{client_ip}"

    attempts = redis_client.incr(key)

    if attempts == 1:
        redis_client.expire(
            key,
            LOGIN_RATE_WINDOW_SECONDS,
        )

    if attempts > LOGIN_RATE_LIMIT:
        ttl = redis_client.ttl(key)

        if ttl < 0:
            ttl = LOGIN_RATE_WINDOW_SECONDS

        return ttl

    return None
