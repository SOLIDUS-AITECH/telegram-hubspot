# FROM python:3.11-slim

# WORKDIR /

# COPY PushHubspot/requirements.txt PushHubspot/requirements.txt

# RUN pip install --no-cache-dir -r PushHubspot/requirements.txt

# COPY . .

# EXPOSE 8002

# CMD ["python", "PushHubspot/run.py"]
FROM python:3.12

WORKDIR /app

COPY PushHubspot/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY PushHubspot /app

EXPOSE 8002

CMD ["python", "run.py"]