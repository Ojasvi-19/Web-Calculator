# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /Calculator

# Copy project files into the container
COPY . /Calculator

# Install system dependencies (needed for PyInstaller & some Python libs)
RUN apt-get update && \
    apt-get install -y binutils && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r Requirements.txt

# Expose Flask port
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=Calculator.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]
