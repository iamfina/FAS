FROM python:3.6

RUN apt-get install -y postgresql-dev
RUN pip install --upgrade pip
RUN pip install psycopg2-binary==2.7.5
RUN pip install numpy==1.15.0

RUN mkdir /app && cd /app
WORKDIR /app

COPY ./requirements.txt /var/tmp/requirements.txt
RUN pip install -r /var/tmp/requirements.txt

COPY ./ /app/
