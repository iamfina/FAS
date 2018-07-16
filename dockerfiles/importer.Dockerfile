FROM python:3.6-alpine

RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache --virtual .build-deps python3-dev gcc libc-dev
RUN pip install psycopg2-binary==2.7.5
RUN apk del .build-deps

RUN mkdir /app && cd /app
WORKDIR /app

COPY ./requirements.txt /var/tmp/requirements.txt
RUN pip install -r /var/tmp/requirements.txt

COPY ./ /app/
