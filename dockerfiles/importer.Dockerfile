FROM python:3.6-alpine

RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache --virtual .build-deps python3-dev gcc libc-dev
RUN pip install psycopg2-binary==2.7.5
RUN pip install numpy==1.15.0

RUN mkdir /app && cd /app
WORKDIR /app

COPY ./requirements.txt /var/tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /var/tmp/requirements.txt
RUN apk del .build-deps

COPY ./ /app/
