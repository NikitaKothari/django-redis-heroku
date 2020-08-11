from myapp.models import MyModel
from myproject.celery import app

import structlog

log = structlog.get_logger()

from celery import Task


@app.task
def counter():
    log.info("test test test")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    instance.save()
