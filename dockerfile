FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt upgrade -y && apt install -y python3 python3-pip
RUN pip3 install chronyk rethinkdb inotify pyyaml fluentbit-server-py 
COPY dist/feedo-0.1.0.tar.gz /tmp/feedo-0.1.0.tar.gz
RUN pip3 install /tmp/feedo-0.1.0.tar.gz
COPY tests/ /root/tests