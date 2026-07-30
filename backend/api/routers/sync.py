from celery.result import AsyncResult
from fastapi import APIRouter, status

from backend.celery_app import celery_app
from backend.tasks.sync_tasks import (
    sync_codeforces,
    sync_leetcode,
)

router = APIRouter(
    prefix="/sync",
    tags=["Sync"],
)


@router.post("/codeforces", status_code=status.HTTP_202_ACCEPTED)
def trigger_codeforces_sync():
    """
    Queue a background task to synchronize a user's Codeforces data.
    """

    user_id = 4  # Temporary until JWT authentication is implemented

    task = sync_codeforces.delay(user_id)

    return {
        "task_id": task.id,
        "status": "queued",
    }


@router.post("/leetcode", status_code=status.HTTP_202_ACCEPTED)
def trigger_leetcode_sync():
    """
    Queue a background task to synchronize a user's LeetCode data.
    """

    user_id = 2  # Temporary until JWT authentication is implemented

    task = sync_leetcode.delay(user_id)

    return {
        "task_id": task.id,
        "status": "queued",
    }


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """
    Retrieve the status of a Celery task.
    """

    task = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task.id,
        "state": task.state,
    }

    if task.state == "SUCCESS":
        response["result"] = task.result

    elif task.state == "FAILURE":
        response["error"] = str(task.result)

    return response
