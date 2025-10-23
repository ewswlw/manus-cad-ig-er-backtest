# Production Dockerfile for CAD-IG Trading Strategy
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config/ ./config/
COPY setup.py .
COPY README.md .

# Install package
RUN pip install --no-cache-dir .

# Create necessary directories
RUN mkdir -p /app/data/raw \
    /app/data/processed \
    /app/models/registry \
    /app/results \
    /app/logs \
    /app/cache

# Create non-root user
RUN useradd -m -u 1000 trader && \
    chown -R trader:trader /app

# Switch to non-root user
USER trader

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import cad_ig_trading; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "cad_ig_trading"]

