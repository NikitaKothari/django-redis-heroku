from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.apps import apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
app = Celery("screenmatter")

app.config_from_object("django.conf:settings")

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
