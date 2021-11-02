FROM python:3.9

WORKDIR /code/

COPY . /code

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
