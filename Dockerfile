# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system deps required by some DB drivers and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements (make sure you have requirements.txt in project root)
COPY requirements.txt /app/requirements.txt

# Install Python deps
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Expose port
EXPOSE 8000

# Default command (development). For production remove --reload
CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]