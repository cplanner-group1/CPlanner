release: python manage.py migrate
web: python
django: gunicorn -b 127.0.0.1:8000 CPlannar.wsgi --log-file -