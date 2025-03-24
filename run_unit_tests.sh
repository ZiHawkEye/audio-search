# Ensure you are using python 3.9 with venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt

cd frontend
npm install
cd ..

# Run backend unit tests
cd backend 
python -m pytest tests/test_app.py

# Run frontend unit tests
cd ../frontend
npx vitest