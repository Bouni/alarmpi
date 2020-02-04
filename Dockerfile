FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update
RUN apk add \
        git \
        curl \
        bash


RUN mkdir /alarmpi
RUN mkdir /config

COPY ./alarmpi/* /alarmpi/

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

