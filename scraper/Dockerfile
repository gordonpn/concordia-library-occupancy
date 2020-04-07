FROM python:3.7-alpine

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN adduser -S -D appuser
WORKDIR /home/appuser
USER appuser

COPY logging.ini .
COPY data_scraper.py .

CMD [ "python", "./data_scraper.py" ]
