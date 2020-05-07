from myapp.models import MyModel
from myproject.celery import app

from myapp.redis import client

@app.task
def counter():
    instance, created = MyModel.objects.get_or_create(id=1)
    instance.counter += 1
    client.set(instance.counter, "tets")
    instance.save()
