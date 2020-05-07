release: python manage.py migrate
web: gunicorn myproject.wsgi --log-file -
worker: celery worker -A myproject -l info
beat: celery beat -A myproject -l info
