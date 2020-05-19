from myapp.models import MyModel
from myproject.celery import app

from myapp.redis import client
import structlog

from celery.task.schedules import crontab
from celery.task import periodic_task

log = structlog.get_logger()

@app.task
def counter():
    log.info("test test test")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter1():
    log.info("counter1")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter2():
    log.info("counter2")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.get(instance.counter)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter3():
    log.info("counter3")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter4():
    log.info("counter4")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter5():
    log.info("counter5")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.get(instance.counter)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter6():
    log.info("counter6")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter7():
    log.info("counter7")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter8():
    log.info("counter8")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter9():
    log.info("counter9")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()

@periodic_task(run_every=crontab(minute="*"))
def counter10():
    log.info("counter10")
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "test", 24 * 3600)
    instance.save()