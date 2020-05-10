release: python manage.py migrate
web: gunicorn myproject.wsgi --log-file -
worker: celery worker -A myproject -l info --pool=gevent --without-gossip -O fair -c 20 --maxtasksperchild=5000
beat: celery beat -A myproject -l info