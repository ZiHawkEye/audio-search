from flask import Flask, render_template, request, jsonify
import whisper
import os
import tempfile
import sqlite3
from pydub import AudioSegment

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
        transcriptions = conn.execute(f'''INSERT INTO transcriptions (title, content) VALUES ('{tmp_file_path}', '{transcription}')''').fetchall()
        conn.close()
        return jsonify({'transcription': transcription}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary file
        os.remove(tmp_file_path)

@app.route('/transcriptions', methods=['GET'])
def transcriptions():
    # Retrieves all transcriptions from the database
    conn = get_db_connection()
    transcriptions = conn.execute('SELECT * FROM transcriptions').fetchall()
    conn.close()
    return render_template('transcriptions.html', posts=transcriptions)

@app.route('/search', methods=['GET'])
def search():
    # Performs a full-text search on transcriptions based on audio file name. (You are given 3 audio files to use for this assignment)

    return 'Status of the service', 200

if __name__ == '__main__':
    app.run(debug=True)