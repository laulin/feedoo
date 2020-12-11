FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt upgrade -y && apt install -y python3 python3-pip
RUN pip3 install chronyk rethinkdb inotify pyyaml fluentbit-server-py 
RUN useradd -m -u 1000 -s /usr/bin/bash user
COPY etc/ /etc/feedoo
COPY dist/feedoo-*.tar.gz /tmp/feedoo.tar.gz
RUN pip3 install /tmp/feedoo.tar.gz
COPY tests/ /root/tests