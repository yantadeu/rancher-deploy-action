FROM python:3.8

COPY . /
WORKDIR /

RUN pip install -r requirements.txt

CMD python deploy_to_rancher.py
