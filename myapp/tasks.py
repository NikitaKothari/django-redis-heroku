from myapp.models import MyModel
from myproject.celery import app

from myapp.redis import client
import structlog

from celery.task.schedules import crontab
from celery.decorators import periodic_task

log = structlog.get_logger()

@app.task
def counter():
    log.info("test test test")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test")
    instance.save()

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_save_latest_flickr_image",
    ignore_result=True
)
def counter1():
    log.info("counter1")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test")
    instance.save()

@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="task_save_latest_flickr_image",
    ignore_result=True
)
def counter2():
    log.info("counter2")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.get(instance.counter)
    instance.save()


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name="task_save_latest_flickr_image",
    ignore_result=True
)
def counter3():
    log.info("counter3")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test")
    instance.save()
