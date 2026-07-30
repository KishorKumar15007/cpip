import os

from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "cpip",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["backend.tasks.sync_tasks"],
)

celery_app.conf.beat_schedule = {
    "schedule-codeforces-sync": {
        "task": "backend.tasks.sync_tasks.schedule_codeforces_sync",
        "schedule": crontab(hour=0, minute=0),
    },
}

celery_app.conf.timezone = "UTC"
