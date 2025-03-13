# Use official Python image as base
FROM python:3.9-slim

# Set workingirectory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create a non-root user for security and set permissions
RUN adduser --disabled-password --gecos "" appuser && \
	mkdir -p /app/database && \
	chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1

# Expose port for web interface
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
# CMD ["uvicorn", "interface.web:app", "--host", "0.0.0.0", "--port", "8000"]