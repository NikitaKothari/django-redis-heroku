from myapp.models import MyModel
from myproject.celery import app

import structlog

log = structlog.get_logger()

from celery import Task


class MyTask(Task):
    ignore_result = True

    def run(self, source, *args, **kwargs):
        log.info("Task ****** Task")
        instance, created = MyModel.objects.get_or_create(id=1)
        instance.counter += 5
        instance.save()


task = MyTask()
app.tasks.register(task)


@app.task
def counter():
    log.info("test test test")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    instance.save()
