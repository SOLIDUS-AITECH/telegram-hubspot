FROM python:3.12

WORKDIR /app

COPY PushHubspot/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY PushHubspot /app

EXPOSE 8002

CMD ["python", "run.py"]