# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg tesseract-ocr

# Print the contents of requirements.txt for debugging purposes
RUN cat /app/requirements.txt

# Install some common dependencies first
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    Pillow \
    google-generativeai \
    numpy \
    scipy \
    opencv-python

# Install the rest of the dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
