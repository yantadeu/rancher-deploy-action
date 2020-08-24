FROM python:3.8

COPY . /

RUN chmod +x /entrypoint.sh
RUN pip install -r /requirements.txt

CMD python /deploy_to_rancher.py

ENTRYPOINT [ "/entrypoint.sh" ]
