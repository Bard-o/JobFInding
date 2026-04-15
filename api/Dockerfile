# Base image with Python 3.12 and minimal packages
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /api

# Copy the requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run FastAPI with uvicorn on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
