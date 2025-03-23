# Reference: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
# Reference: https://thedavidmasters.com/2024/09/11/how-to-build-and-run-a-flask-api-with-openais-whisper-local-model-using-docker/

import logging
from flask import Flask, render_template, request, jsonify
import whisper
import os
import tempfile
import sqlite3
from pydub import AudioSegment
from flask_cors import CORS, cross_origin
from init_db import init_db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Get allowed origins from environment variable, change if frontend is not locally hosted
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')  

CORS(app, resources={
    r"/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

model = whisper.load_model("tiny")

def get_db_connection():
    # Gets the SQL DB connection
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

    result = model.transcribe(file_path)
    return result['text']

@app.route('/transcribe', methods=['POST'])
@cross_origin()
def transcribe():
    # Accepts audio files, performs transcription and saves results in database.
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    filename = request.form['filename']

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        audio_file.save(tmp_file.name)
        tmp_file_path = tmp_file.name
    try:
        transcription = transcribe_audio(tmp_file_path)

        conn = get_db_connection()
        conn.execute('INSERT INTO transcriptions (title, content) VALUES (?, ?)', (filename, transcription))
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
    conn.commit()
    conn.close()

    transcriptions_list = [{'id': row[0], 'created': row[1], 'title': row[2], 'content': row[3]} for row in transcriptions]
    
    return jsonify(transcriptions=transcriptions_list), 200

@app.route('/delete', methods=['DELETE'])
@cross_origin()
def delete():
    # Delete transcription
    id = request.args.get('id')

    if not id:
        return jsonify({'error': 'No transcription ID provided'}), 400

    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM transcriptions WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Transcription deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    # Performs a full-text search on transcriptions based on audio file name. (You are given 3 audio files to use for this assignment)
    title = request.args.get('title')
    logging.info(f'Received search title: {title}')  # Log the title

    conn = get_db_connection()
    transcriptions = conn.execute('SELECT * FROM transcriptions WHERE LOWER(title) LIKE LOWER(?)', ('%' + title.strip() + '%',)).fetchall()
    conn.commit()
    conn.close()

    logging.info(f'Found transcriptions: {transcriptions}')

    transcriptions_list = [{'id': row[0], 'created': row[1], 'title': row[2], 'content': row[3]} for row in transcriptions]
    
    return jsonify(transcriptions=transcriptions_list), 200

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)