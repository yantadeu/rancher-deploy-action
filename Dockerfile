FROM python:3.8

COPY . /

RUN echo 'teste'
RUN chmod +x /entrypoint.sh
RUN pip install -r /requirements.txt

ENTRYPOINT [ "/entrypoint.sh" ]
