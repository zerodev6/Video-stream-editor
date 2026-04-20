# Use an optimized Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# ffmpeg: The core engine for video editing
# libsm6, libxext6: Common libraries for media processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create the downloads directory
RUN mkdir -p downloads

# Command to run the bot
CMD ["python3", "main.py"]

