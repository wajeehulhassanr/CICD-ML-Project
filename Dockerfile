# Use official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY src/ .

# Expose Flask's default port
EXPOSE 5000

# Set the command to run the application
CMD ["python", "app.py"]