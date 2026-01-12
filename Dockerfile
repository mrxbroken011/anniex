FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y ffmpeg curl git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && node -v \
    && npm -v

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD bash start
