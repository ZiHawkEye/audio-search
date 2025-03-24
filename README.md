# audio-search

A full stack app for transcribing and searching audio files.

## Development Setup

### Required Dependencies

#### Backend
- Python 3.9+
- Docker

#### Frontend
- Node.js 18+
- npm 10+

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/ZiHawkEye/audio-search.git
cd audio-search
```

2. Create and activate a virtual environment to install backend dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt
```

3. Install frontend dependencies
```
# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Running the Application

### Backend

1. Start the backend server in a Docker container:
```
bash run_backend_container.sh
```

The backend API will be available at `http://localhost:5000`

### Frontend

1. Start the frontend server in a Docker container:
```
bash run_frontend_container.sh
```

The frontend will be available at `http://localhost:8080`

## Running Tests

### Unit Tests

1. Ensure you're in the project root and your Python virtual environment is activated, as well as installed the required dependencies for both frontend and backend
```bash
# Run all unit tests
bash run_unit_tests.sh
```