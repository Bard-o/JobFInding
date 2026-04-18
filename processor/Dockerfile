# Base image with Python 3.12
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /processor

# Copy the requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download both English and Spanish medium spaCy models
RUN python -m spacy download en_core_web_md
RUN python -m spacy download es_core_news_md

# Copy the rest of the application code
COPY . .

# Default command to run the processing pipeline
CMD ["python", "main.py"]
