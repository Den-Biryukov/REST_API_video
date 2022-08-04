FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN ["mkdir", "/rest_api_video"]
WORKDIR /rest_api_video
ADD . /rest_api_video
RUN pip install -r requirements.txt