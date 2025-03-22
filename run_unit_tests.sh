# Ensure you are using python 3.9 with venv

# Run backend unit tests
cd backend 
python -m pytest tests/test_app.py

# Run frontend unit tests
cd ../frontend
npx vitest