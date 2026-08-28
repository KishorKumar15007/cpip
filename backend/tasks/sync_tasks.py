import os
from celery.utils.log import get_task_logger
from httpx import HTTPError

from backend.celery_app import celery_app
from backend.db.session import SessionLocal
from backend.models.user import User
from backend.services.codeforces.client import CodeforcesClient
from backend.services.codeforces.sync import CodeforcesSyncService
from backend.services.leetcode.client import LeetCodeClient
from backend.services.leetcode.sync import LeetCodeSyncService
from backend.tasks.locks import user_sync_lock

logger = get_task_logger(__name__)


@celery_app.task(
    autoretry_for=(HTTPError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def sync_codeforces(user_id: int):
    """
    Background task to synchronize a user's Codeforces data.
    """

    with user_sync_lock("codeforces", user_id) as acquired:
        if not acquired:
            logger.info(
                f"Codeforces sync already running for user {user_id}"
            )
            return {
                "status": "already_running",
            }

        logger.info(f"Starting Codeforces sync for user {user_id}")

        session = SessionLocal()

        try:
            client = CodeforcesClient()
            service = CodeforcesSyncService(client)

            result = service.sync_all(
                session=session,
                user_id=user_id,
            )

            logger.info(
                f"Finished Codeforces sync for user {user_id}: {result}"
            )

            return result

        except Exception:
            logger.exception(
                f"Codeforces sync failed for user {user_id}"
            )
            raise

        finally:
            client.close()
            session.close()


@celery_app.task(
    autoretry_for=(HTTPError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def sync_leetcode(user_id: int):
    """
    Background task to synchronize a user's LeetCode data.
    """

    with user_sync_lock("leetcode", user_id) as acquired:
        if not acquired:
            logger.info(
                f"LeetCode sync already running for user {user_id}"
            )
            return {
                "status": "already_running",
            }

        logger.info(f"Starting LeetCode sync for user {user_id}")

        session = SessionLocal()

        try:
            client = LeetCodeClient(
                session_cookie=os.getenv("LEETCODE_SESSION"),
                csrf_token=os.getenv("LEETCODE_CSRF_TOKEN"),
            )

            service = LeetCodeSyncService(client)

            result = service.sync_all(
                session=session,
                user_id=user_id,
            )

            logger.info(
                f"Finished LeetCode sync for user {user_id}: {result}"
            )

            return result

        except Exception:
            logger.exception(
                f"LeetCode sync failed for user {user_id}"
            )
            raise

        finally:
            client.close()
            session.close()


@celery_app.task
def schedule_codeforces_sync():
    db = SessionLocal()

    try:
        users = (
            db.query(User)
            .filter(
                User.cf_username.isnot(None),
                User.cf_username != "",
            )
            .all()
        )

        queued = 0

        for user in users:
            sync_codeforces.delay(user.user_id)
            queued += 1

        logger.info(f"Queued Codeforces sync for {queued} users.")

        return {
            "queued_users": queued,
        }

    finally:
        db.close()
