cd frontend

# Build Docker image
docker build -t my-vue-app .

# Run Docker image
docker run -p 8080:80 my-vue-app