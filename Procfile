release: python manage.py migrate
web: bin/start-nginx gunicorn -c config/gunicorn.conf.py myproject.wsgi --log-file -
worker: celery worker -A myproject -l info --without-gossip -O fair -c 20 --maxtasksperchild=5000
beat: celery beat -A myproject -l info
