from contextlib import contextmanager

from backend.redis_client import redis_client


SYNC_COOLDOWN_SECONDS = 5 * 60


@contextmanager
def user_sync_lock(platform: str, user_id: int):
    lock = redis_client.lock(
        f"sync:{platform}:{user_id}",
        timeout=600,
    )

    acquired = lock.acquire(blocking=False)

    try:
        yield acquired
    finally:
        if acquired:
            lock.release()


def acquire_sync_cooldown(
    platform: str,
    user_id: int,
) -> int | None:
    key = f"sync:cooldown:{platform}:{user_id}"

    acquired = redis_client.set(
        key,
        "1",
        nx=True,
        ex=SYNC_COOLDOWN_SECONDS,
    )

    if acquired:
        return None

    retry_after = redis_client.ttl(key)

    if retry_after < 0:
        retry_after = SYNC_COOLDOWN_SECONDS

    return retry_after
