cd backend

# Build Docker image
docker build -t my-python-app .

# Run Docker image
docker run -p 5000:5000 my-python-app