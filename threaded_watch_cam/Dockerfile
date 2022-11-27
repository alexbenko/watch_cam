FROM arm64v8/debian:bullseye
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONIOENCODING=utf-8

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y locales

RUN apt-get install sox -y
RUN apt-get install libsox-fmt-mp3 -y
RUN apt-get install python3-gst-1.0 -y

#RUN apt-get install tesseract-ocr

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE $PORT

CMD python3 app.py