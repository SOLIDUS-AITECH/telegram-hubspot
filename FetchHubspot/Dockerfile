# FROM python:3.11-slim

# WORKDIR /

# COPY FetchHubspot/requirements.txt FetchHubspot/requirements.txt

# RUN pip install --no-cache-dir -r FetchHubspot/requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["python", "FetchHubspot/run.py"]

FROM python:3.12

WORKDIR /app

COPY FetchHubspot/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY FetchHubspot /app

EXPOSE 8000

CMD ["python", "run.py"]