# Reference: https://flask.palletsprojects.com/en/stable/testing/

import pytest
from flask import Flask
from ..app import app
from ..init_db import init_db

# Creates a fixture function to initialise client
@pytest.fixture
def client():
    # Use "with" to ensure client setup and teardown
    # Ensures sequential tests do not share state
    with app.test_client() as client:
        # init_db()
        yield client

def test_health(client):
    # Test for /health
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "Service is healthy"}

def test_transcribe(client):
    # Test for /transcribe 
    with open('..//HTX xData Technical Test (SWE) audio_samples/Sample 1.mp3', 'rb') as audio_file :
        response = client.post('transcribe', data={
            'audio': audio_file,
            'filename': 'test_audio.mp3'
        })
        print(response.json)
        assert response.status_code == 200
        assert 'transcription' in response.json

def test_search(client):
    # Test /search
    title = 'test_audio'
    response = client.get(f'/search?title={title}')
    assert response.status_code == 200
    assert 'transcriptions' in response.json

def test_delete(client):
    # Test /delete 
    id = 1
    response = client.delete(f'/delete?id={id}')
    assert response.status_code == 200
