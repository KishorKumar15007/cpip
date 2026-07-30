from contextlib import contextmanager

from backend.redis_client import redis_client


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
