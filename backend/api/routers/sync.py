from celery.result import AsyncResult

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from backend.api.dependencies import get_current_user
from backend.celery_app import celery_app
from backend.models.user import User
from backend.redis_client import redis_client
from backend.tasks.locks import acquire_sync_cooldown
from backend.tasks.sync_tasks import (
    sync_codeforces,
    sync_leetcode,
)


router = APIRouter(
    prefix="/sync",
    tags=["Sync"],
)


TASK_OWNERSHIP_SECONDS = 60 * 60


def store_task_owner(
    task_id: str,
    user_id: int,
):
    redis_client.set(
        f"sync:task_owner:{task_id}",
        str(user_id),
        ex=TASK_OWNERSHIP_SECONDS,
    )


@router.post(
    "/codeforces",
    status_code=status.HTTP_202_ACCEPTED,
)
def trigger_codeforces_sync(
    current_user: User = Depends(get_current_user),
):
    """
    Queue a background task to synchronize
    the current user's Codeforces data.
    """

    retry_after = acquire_sync_cooldown(
        "codeforces",
        current_user.user_id,
    )

    if retry_after is not None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                "Codeforces sync was recently triggered. "
                "Try again later."
            ),
            headers={
                "Retry-After": str(retry_after),
            },
        )

    task = sync_codeforces.delay(
        current_user.user_id
    )

    store_task_owner(
        task.id,
        current_user.user_id,
    )

    return {
        "task_id": task.id,
        "status": "queued",
    }


@router.post(
    "/leetcode",
    status_code=status.HTTP_202_ACCEPTED,
)
def trigger_leetcode_sync(
    current_user: User = Depends(get_current_user),
):
    """
    Queue a background task to synchronize
    the current user's LeetCode data.
    """

    retry_after = acquire_sync_cooldown(
        "leetcode",
        current_user.user_id,
    )

    if retry_after is not None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                "LeetCode sync was recently triggered. "
                "Try again later."
            ),
            headers={
                "Retry-After": str(retry_after),
            },
        )

    task = sync_leetcode.delay(
        current_user.user_id
    )

    store_task_owner(
        task.id,
        current_user.user_id,
    )

    return {
        "task_id": task.id,
        "status": "queued",
    }


@router.get(
    "/tasks/{task_id}",
)
def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the status of a Celery task owned
    by the current user.
    """

    owner = redis_client.get(
        f"sync:task_owner:{task_id}"
    )

    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    if int(owner) != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    task = AsyncResult(
        task_id,
        app=celery_app,
    )

    response = {
        "task_id": task.id,
        "state": task.state,
    }

    if task.state == "SUCCESS":
        response["result"] = task.result

    elif task.state == "FAILURE":
        response["error"] = (
            "The sync task failed."
        )

    return response
