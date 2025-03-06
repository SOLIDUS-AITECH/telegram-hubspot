# FROM python:3.11-slim

# WORKDIR /

# COPY TelegramHubspotIntegration/requirements.txt TelegramHubspotIntegration/requirements.txt

# RUN pip install --no-cache-dir -r TelegramHubspotIntegration/requirements.txt

# COPY . .

# EXPOSE 8003

# CMD ["python", "TelegramHubspotIntegration/run.py"]
FROM python:3.12

WORKDIR /app

COPY TelegramHubspotIntegration/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY TelegramHubspotIntegration /app

EXPOSE 8003

CMD ["python", "run.py"]