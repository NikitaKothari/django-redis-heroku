from __future__ import absolute_import, unicode_literals
import celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
app = celery.Celery("connect")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
