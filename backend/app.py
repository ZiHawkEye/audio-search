# Reference: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
# Reference: https://thedavidmasters.com/2024/09/11/how-to-build-and-run-a-flask-api-with-openais-whisper-local-model-using-docker/

from flask import Flask, render_template, request, jsonify
import whisper
import os
import tempfile
import sqlite3
from pydub import AudioSegment
from flask_cors import CORS, cross_origin

app = Flask(__name__)


# Load the Whisper model when the app starts
model = whisper.load_model("base")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health', methods=['GET'])
def health():
    # Returns the status of the service
    return jsonify(status='Service is healthy'), 200

def transcribe_audio(file_path):
    # Convert the file to WAV format if necessary
    audio = AudioSegment.from_file(file_path)
    if file_path.split('.')[-1] != 'wav':
        file_path = file_path.rsplit('.', 1)[0] + '.wav'
        audio.export(file_path, format='wav')

    # Transcribe the audio file using the local Whisper model
    result = model.transcribe(file_path)
    return result['text']

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Accepts audio files, performs transcription and save results in database.
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        audio_file.save(tmp_file.name)
        tmp_file_path = tmp_file.name
    try:
        # Transcribe the audio file
        transcription = transcribe_audio(tmp_file_path)
        # Insert transcription to database
        conn = get_db_connection()
        conn.execute('INSERT INTO transcriptions (title, content) VALUES (?, ?)', (tmp_file_path, transcription))
        conn.commit()
        conn.close()

        return jsonify({'transcription': transcription}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(tmp_file_path)

@app.route('/transcriptions', methods=['GET'])
@cross_origin()
def transcriptions():
    # Retrieves all transcriptions from the database
    conn = get_db_connection()
    transcriptions = conn.execute('SELECT * FROM transcriptions').fetchall()
    conn.close()
    # Convert the fetched data to a list of dictionaries for JSON serialization
    transcriptions_list = [{'id': row[0], 'title': row[2], 'content': row[3]} for row in transcriptions]
    
    return jsonify(transcriptions=transcriptions_list), 200

@app.route('/search', methods=['GET'])
def search():
    # Performs a full-text search on transcriptions based on audio file name. (You are given 3 audio files to use for this assignment)

    return 'Status of the service', 200

if __name__ == '__main__':
    app.run(debug=True)