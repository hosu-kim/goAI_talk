FROM python:3.10-slim

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory and set permissions
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Volume for storing database files
VOLUME /app/data

# Set environment variables
ENV DB_PATH=/app/data/football_data.db
# Note: API keys should be provided at runtime

# Expose the web server port
EXPOSE 8000

# Run web interface by default (modified to match your application)
CMD ["python", "main.py", "--update"]