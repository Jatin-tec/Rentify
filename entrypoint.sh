#!/bin/bash

# Apply database migrations
python manage.py makemigrations --no-input
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn server
gunicorn rentify.wsgi:application --bind 0.0.0.0:8000
