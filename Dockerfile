#this is running on a raspberry pi with Ubuntu as the OS
FROM arm64v8/ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD ["app.py", "--ip 0.0.0.0", " --port 5000"]