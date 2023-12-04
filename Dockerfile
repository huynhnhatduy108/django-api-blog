FROM python:3.11.4-slim-buster

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install app dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .

EXPOSE 8000

# python manage.py makemigrations models
# python manage.py migrate
# python manage.py runserver 0.0.0.0:8000





