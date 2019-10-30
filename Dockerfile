FROM python:3

RUN apt-get update

RUN apt-get install libopus0

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
