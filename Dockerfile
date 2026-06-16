# Multi-stage build for optimized production image
FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy AS builder

WORKDIR /app

# Install system dependencies for video/audio processing and OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (needed for web automation)
RUN playwright install chromium && \
    playwright install-deps chromium

# Copy application code
COPY . .

# Create required directories for the pipeline
RUN mkdir -p /app/videos /app/frames /app/jsons /app/sessions && \
    chmod 755 /app/videos /app/frames /app/jsons /app/sessions

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

LABEL maintainer="Job Scraper Team"
LABEL description="Multimodal Job Extractor - Instagram Reels to Structured Job Data Pipeline"
LABEL version="1.0"

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy from builder stage
COPY --from=builder /app /app
COPY --from=builder /root/.cache /root/.cache

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Health check to verify container is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Run the application
CMD ["python", "main.py"]