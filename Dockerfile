# Use a slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system packages for supervisor
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose Flask port
EXPOSE 8080

# Start Supervisor to run both services
CMD ["supervisord", "-c", "/app/supervisord.conf"]
