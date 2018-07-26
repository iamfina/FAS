FROM python:3.6

RUN apt-get install -y libpq-dev
RUN pip install --upgrade pip

RUN mkdir /app && cd /app
WORKDIR /app

COPY ./requirements.txt /var/tmp/requirements.txt
RUN pip install -r /var/tmp/requirements.txt

COPY ./ /app/
