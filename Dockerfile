# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install ffmpeg for audio processing
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Whisper and other Python dependencies
# RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]