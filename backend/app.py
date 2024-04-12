from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send
import speech_recognition as sr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
# socketio = SocketIO(app)

# Apply CORS middleware to your Flask app
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173/"}})

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech(audio_data):
    try:
        # Recognize speech using Google Speech Recognition
        with sr.AudioFile(audio_data) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Request error: {e}"

@socketio.on('audio-stream')
def handle_audio_stream(audio_chunk):
    try:
        # Recognize speech from audio chunk
        transcription = recognize_speech(audio_chunk)
        # Send back transcription
        send(transcription)
    except Exception as e:
        send(str(e))

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    try:
        # Get audio file from request
        audio_file = request.files['audio']

        # Save audio file temporarily
        temp_audio_path = 'temp_audio.wav'
        audio_file.save(temp_audio_path)

        # Recognize speech from audio file
        transcription = recognize_speech(temp_audio_path)

        # Return transcription
        return jsonify({'transcription': transcription})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)
