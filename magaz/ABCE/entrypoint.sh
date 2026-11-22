#!/bin/sh
python manage.py collectstatic --noinput
# Разрешаем всем читать файлы и заходить в папки
chmod -R a+rX /app/staticfiles
exec gunicorn ABCE.wsgi:application --bind 0.0.0.0:8000