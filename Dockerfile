FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /diu

ADD . /diu

COPY ./requirements.txt /diu/requirements.txt

RUN pip install -r requirements.txt

COPY . /diu
