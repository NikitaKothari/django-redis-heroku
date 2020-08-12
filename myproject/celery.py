from __future__ import absolute_import, unicode_literals
import celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
app = celery.Celery("connect")

app.config_from_object("django.conf:settings")

from django.apps import apps

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
