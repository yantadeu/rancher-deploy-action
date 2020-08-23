FROM python:3.8

COPY . /app
WORKDIR /app

RUN chmod +x entrypoint.sh
RUN pip install -r requirements.txt

ENTRYPOINT [ "bash", "entrypoint.sh" ]
