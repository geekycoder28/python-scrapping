FROM ubuntu:18.04
MAINTAINER Wakahiu Njenga <wakahiu.njenga@gmail.com>

# Update the image to the latest packages
RUN apt-get update && apt-get upgrade -y

# Install app dependencies
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

COPY . /app
WORKDIR "/app"

# Install pip requirements
RUN pip3 install -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=./app/proxima-media-a9b18d9e8127.json
ENV REDIS_HOST=10.7.107.171
ENV REDIS_PORT=6379
ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8

ENTRYPOINT python3 ./app/main.py
