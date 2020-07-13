"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = get_wsgi_application()

# required to make nginx serve traffic. see https://github.com/heroku/heroku-buildpack-nginx#applicationdyno-coordination
from pathlib import Path

Path("/tmp/app-initialized").touch()
