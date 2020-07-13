release: python manage.py migrate
web: bin/start-nginx gunicorn --preload myproject.wsgi --bind 127.0.0.1:$DJANGO_PORT
worker: celery worker -A myproject -l info --without-gossip -O fair -c 20 --maxtasksperchild=5000
beat: celery beat -A myproject -l info
