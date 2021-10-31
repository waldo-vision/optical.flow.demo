FROM python:3.8

WORKDIR /code

COPY /opticalFlow /code

RUN pip install -r requirements.txt
