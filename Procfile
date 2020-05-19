release: python manage.py migrate
web: bin/start-twemproxy gunicorn myproject.wsgi --log-file -
worker: bin/start-twemproxy celery worker -A myproject -l info --without-gossip -O fair -c 20 --maxtasksperchild=5000
beat: bin/start-twemproxy celery beat -A myproject -l info
