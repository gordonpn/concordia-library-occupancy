FROM python:3.8-alpine

RUN adduser \
  --disabled-password \
  --home /home/appuser \
  --shell /bin/bash \
  --system \
  --uid 1000 \
  appuser

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN chown appuser /home/appuser

WORKDIR /home/appuser
USER appuser

COPY . .

CMD ["python", "./main.py"]
