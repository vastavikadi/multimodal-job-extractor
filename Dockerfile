FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app

# Install additional dependencies for video processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install Playwright browsers
RUN playwright install chromium

CMD ["python", "main.py"]