FROM python:3.6.5

COPY requirements.txt /usr/src
COPY jenkins-cli.jar /usr/src
COPY jre-8u181-linux-x64.tar.gz /usr/src

RUN tar xvf /usr/src/jre-8u181-linux-x64.tar.gz -C /usr/src
RUN pip install --no-cache-dir -r /usr/src/requirements.txt

RUN mkdir -p /usr/src/download
RUN mkdir -p /usr/src/upload

ENV PATH=$PATH:/usr/src/jre1.8.0_181/bin
ENV PYTHONPATH=/usr/src:$PYTHONPATH

WORKDIR /usr/src
