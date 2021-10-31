FROM python:3.8

WORKDIR /code

COPY /opticalFlow /code

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
