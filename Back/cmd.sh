celery -A app.celery worker --loglevel=info
celery -A app.celery beat --loglevel=info
