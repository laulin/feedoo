FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt upgrade -y && apt install -y python3 python3-pip htop
RUN pip3 install chronyk rethinkdb inotify pyyaml fluentbit-server-py dnspython pyahocorasick
RUN useradd -m -u 1000 -s /usr/bin/bash user
COPY examples/etc/ /etc/feedoo
COPY dist/feedoo-*.tar.gz /tmp/feedoo.tar.gz
RUN pip3 install /tmp/feedoo.tar.gz
COPY examples/plugins/dist/feedoo_hash-*.tar.gz /tmp/feedoo_hash.tar.gz
RUN pip3 install /tmp/feedoo_hash.tar.gz
COPY tests/ /root/tests