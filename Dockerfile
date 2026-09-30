FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    xvfb \
    xauth \
    && rm -rf /var/lib/apt/lists/*

RUN python -m playwright install --with-deps chromium

COPY . .

CMD ["xvfb-run", "--auto-servernum", "--server-args=-screen 0 1280x720x24", "python", "app.py"]