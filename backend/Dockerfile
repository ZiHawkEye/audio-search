# Use an official Python runtime as a parent image
FROM python:3.9

# Install ffmpeg for audio processing
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
# RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for CORS, change if frontend is not locally hosted
ENV ALLOWED_ORIGINS="http://localhost:80"

# Expose port 5000
EXPOSE 5000

# CMD ["python", "app.py"]

# Use gunicorn instead of Flask's development server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]