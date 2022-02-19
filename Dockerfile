FROM python:3

ADD app.py /

RUN pip install redis
RUN pip install prometheus-client

CMD [ "python", "./app.py" ]
