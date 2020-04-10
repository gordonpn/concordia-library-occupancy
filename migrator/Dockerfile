FROM python:3.7-alpine

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN adduser -S -D appuser
WORKDIR /home/appuser
USER appuser

COPY logging.ini .
COPY data_migrator.py .
COPY data.json .

CMD [ "python", "./data_migrator.py" ]
