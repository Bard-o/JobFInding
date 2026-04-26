# Base image with Python 3.12 and minimal packages
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /processor

# Copy the requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the Spanish spaCy model (baked into the image so it doesn't download every run)
RUN python -m spacy download es_core_news_sm

# Copy the rest of the application code
COPY . .

# Command to run the processor
CMD ["python", "main.py"]
