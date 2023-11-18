# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN pip install --upgrade pip

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# COPY chromedriver.exec /usr/bin/chromedriver.exec
# RUN chmod +x /usr/bin/chromedriver.exec

# RUN apt-get update
# RUN apt-get install -y chromium-driver

# copy project
COPY . .