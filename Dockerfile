FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create directory for models
RUN mkdir -p models

# Set environment variables
ENV MODEL_PATH=models/iris_model.joblib
ENV PORT=5000
ENV PYTHONPATH=/app

# Expose port
EXPOSE ${PORT}

# Run the application
CMD ["python", "src/app.py"] 