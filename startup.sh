#!/bin/bash
python3 manage.py makemigrations app api
python3 manage.py migrate
{
    python3 manage.py createsuperuser --noinput
} || {
    echo "User not created"
}
uvicorn moonsuit.asgi:application --port 8080 --host 0.0.0.0 --workers 4