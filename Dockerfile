FROM ubuntu:latest

COPY . /

RUN chmod +x /entrypoint.sh

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip3 install -r /requirements.txt

ENTRYPOINT ["/entrypoint.sh"]