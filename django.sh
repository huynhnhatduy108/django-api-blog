#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations models

echo "Starting Migrations..."
python manage.py migrate

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000