# # pull official base image
# FROM python:3.11.4-slim-buster

# # set work directory
# WORKDIR /usr/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install system dependencies
# RUN apt-get update && apt-get install -y netcat

# # install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# # copy entrypoint.sh
# COPY ./entrypoint.sh .
# RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
# RUN chmod +x /usr/src/app/entrypoint.sh

# # copy project
# COPY . .

# # run entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Используем официальный образ Python в качестве базового образа
FROM python:3.10-alpine3.17

RUN pip install --upgrade pip
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

