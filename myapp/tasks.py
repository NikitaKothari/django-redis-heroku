from myapp.models import MyModel
from myproject.celery import app

from myapp.redis import client
import structlog

log = structlog.get_logger()



@app.task
def counter():
    log.info("test test test")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test")
    log.info(client.info())
    instance.save()

@app.task
def counter1():
    log.info("counter1")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test")
    log.info(client.info())
    instance.save()

@app.task
def counter2():
    log.info("counter2")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.get(instance.counter)
    log.info(client.info())
    instance.save()

@app.task
def counter3():
    log.info("counter3")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test")
    log.info(client.info())
    instance.save()
