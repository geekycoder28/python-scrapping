#
# Ubuntu Dockerfile
#
# https://github.com/dockerfile/ubuntu
#

# Pull base image.
FROM ubuntu:18.04
MAINTAINER Wakahiu Njenga <wakahiu.njenga@gmail.com>

# Update the image to the latest packages
RUN apt-get update && apt-get upgrade -y

# Install app dependencies
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip \
    wget
RUN pip3 install --upgrade pip

# Copy files and change the working directory
COPY . /app
WORKDIR "/app"

# Install pip requirements
RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED=0
ENV PYTHONIOENCODING=utf-8

ENTRYPOINT python3 run.py
