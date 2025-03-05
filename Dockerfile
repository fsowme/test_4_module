FROM python:3.11

RUN mkdir -p /data/app
RUN mkdir -p /data/app/certs

COPY requirements.txt /data/
RUN pip install -r /data/requirements.txt

COPY producer.py /data/app/
COPY consumer.py /data/app/


WORKDIR /data/app
