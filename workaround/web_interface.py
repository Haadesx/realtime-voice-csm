from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit
import numpy as np
import queue
import threading
from fast_chat import record_audio, transcribe_audio, get_cached_response, generate_optimized_speech, play_audio
import sounddevice as sd
import json
import os

app = Flask(__name__)
app.template_folder = os.path.join(os.path.dirname(__file__), 'templates')
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for audio processing
audio_queue = queue.Queue()
stop_recording = threading.Event()
current_audio_data = np.zeros(128)

@app.route('/')
def index():
    return render_template('index.html')

def audio_callback(indata, frames, time, status):
    """This is called for each audio block"""
    if status:
        print(status)
    # We use the RMS value to visualize audio intensity
    audio_data = np.sqrt(np.mean(indata**2, axis=1))
    # Normalize and scale the data
    audio_data = (audio_data * 255 / np.max(audio_data) if np.max(audio_data) > 0 else np.zeros_like(audio_data))
    # Ensure we have 128 points by resampling if necessary
    audio_data = np.interp(np.linspace(0, len(audio_data), 128), np.arange(len(audio_data)), audio_data)
    audio_queue.put(audio_data)

@socketio.on('start_recording')
def handle_recording_start():
    global stop_recording
    stop_recording.clear()
    
    def process_audio():
        try:
            with sd.InputStream(callback=audio_callback):
                while not stop_recording.is_set():
                    if not audio_queue.empty():
                        audio_data = audio_queue.get()
                        socketio.emit('audio_data', {'input': audio_data.tolist()})
                    socketio.sleep(0.05)
        except Exception as e:
            print(f"Error in audio processing: {e}")
            
    threading.Thread(target=process_audio).start()

@socketio.on('stop_recording')
def handle_recording_stop():
    global stop_recording
    stop_recording.set()
    # Clear any remaining data
    while not audio_queue.empty():
        audio_queue.get()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 