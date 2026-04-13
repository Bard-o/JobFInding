# Base image with Python 3.12 and minimal packages
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "main.py"]
