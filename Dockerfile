FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install bash

RUN mkdir /alarmpi
RUN mkdir /config

COPY ./alarmpi/* /alarmpi/

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

