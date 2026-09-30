FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y xvfb

RUN python -m playwright install --with-deps chromium

COPY . .

CMD ["xvfb-run", "-a", "python", "app.py"]