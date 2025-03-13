# FROM python:3.11-slim

# WORKDIR /

# COPY FetchTelegram/requirements.txt FetchTelegram/requirements.txt

# RUN pip install --no-cache-dir -r FetchTelegram/requirements.txt

# COPY . .

# EXPOSE 8001

# CMD ["python", "FetchTelegram/run.py"]
FROM python:3.12

WORKDIR /app

COPY FetchTelegram/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY FetchTelegram /app

EXPOSE 8001

CMD ["python", "run.py"]