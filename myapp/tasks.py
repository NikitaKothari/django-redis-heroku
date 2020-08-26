from myapp.models import MyModel
from myproject.celery import app

import structlog

log = structlog.get_logger()

from celery import Task
import celery
from myapp.redis import client
from django.conf import settings


class MyTask(Task):
    ignore_result = True

    def run(self):
        log.info("Task ****** Task **")
        instance, created = MyModel.objects.get_or_create(id=1)
        instance.counter += 5
        instance.save()


mytask = MyTask()
app.tasks.register(mytask)


class Test:
    def counter(self):
        log.info("test test test")
        instance, created = MyModel.objects.get_or_create(id=1)
        instance.counter += 1
        instance.save()


@app.task
@celery.task
def counter_task():
    client.set("Nikita", 5)
    log.info("---------From Redis----------")
    log.info(settings.REDIS_URL)
    log.info(client.get("Nikita"))
    log.info("---------To Redis----------")
    Test().counter()
