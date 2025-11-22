FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    libffi-dev \
    build-essential \
    curl \
    unzip \
    && apt-get clean

# Install Deno (yt-dlp support)
RUN curl -fsSL https://deno.land/install.sh | sh
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

# Workdir
WORKDIR /app

# Copy bot files
COPY . /app

# Install deps
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Start health server + ping script + bot
CMD python3 app.py & python3 -m anony
