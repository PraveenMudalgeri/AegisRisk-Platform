# Stub celery app
from celery import Celery

celery = Celery("app", broker="redis://redis:6379/0")

celery.conf.task_routes = {
    "app.worker.test_task": "main-queue",
}
