# FROM python:3.12

# WORKDIR /

# COPY TelegramGetAuthToken/requirements.txt TelegramGetAuthToken/requirements.txt

# RUN pip install --no-cache-dir -r TelegramGetAuthToken/requirements.txt

# COPY . .

# EXPOSE 8005

# CMD ["python", "TelegramGetAuthToken/run.py"]
FROM python:3.12

WORKDIR /app

COPY TelegramGetAuthToken/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY TelegramGetAuthToken /app

EXPOSE 8005

CMD ["python", "run.py"]