FROM python:3.13-slim

WORKDIR /app/bot
COPY requirements.txt /app/bot/requirements.txt
RUN pip install --no-cache-dir -r /app/bot/requirements.txt
COPY . /app/bot/

WORKDIR /app/bot

EXPOSE 7777
CMD ["python", "aiogram_run.py"]