FROM python:3.12

WORKDIR /app

COPY FetchHubspot/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY FetchHubspot /app

EXPOSE 8000

CMD ["python", "run.py"]