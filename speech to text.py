import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import ipywidgets as widgets
from IPython.display import display
import numpy as np
import threading
import time
import os
import google.generativeai as genai

# ====== CONFIGURATION ======
SAMPLE_RATE = 44100
AUDIO_FILENAME = "recorded_audio.wav"
GOOGLE_API_KEY = ("AIzaSyAAlb_qqQMJ0dkTR-vtQ1IEJSdx3YgP-jk")  # Replace with your key

# ====== Load Whisper Model ======
model = whisper.load_model("base")

# ====== Global variables ======
recording = False
audio_data = []

# ====== Whisper transcription ======
def transcribe_audio():
    print("Transcribing using Whisper...")
    result = model.transcribe(AUDIO_FILENAME)
    print("\n📝 Whisper Transcription:\n", result['text'])
    send_to_google_gemini(result['text'])

# ====== Google Gemini Pro integration ======
def send_to_google_gemini(prompt_text):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt_text)
    print("\n🤖 Gemini Pro Response:\n", response.text)

# ====== Fixed duration recording ======
def record_fixed_duration(duration=5):
    print(f"🎙️ Recording for {duration} seconds...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    write(AUDIO_FILENAME, SAMPLE_RATE, audio)
    print("✅ Recording saved as:", AUDIO_FILENAME)
    transcribe_audio()

# ====== Manual recording with stop ======
def callback(indata, frames, time, status):
    if recording:
        audio_data.append(indata.copy())

def record_with_stop():
    global recording, audio_data
    audio_data = []
    recording = True

    print("🎙️ Recording started... Click 'Stop' to end.")
    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback)
    with stream:
        while recording:
            time.sleep(0.1)

    audio_np = np.concatenate(audio_data, axis=0)
    write(AUDIO_FILENAME, SAMPLE_RATE, audio_np)
    print("🛑 Recording stopped and saved.")
    transcribe_audio()

def stop_recording(_):
    global recording
    recording = False

# ====== GUI widgets ======
duration_slider = widgets.IntSlider(description='Duration (sec)', value=5, min=1, max=30)
record_fixed_btn = widgets.Button(description='🎧 Record (Fixed)', button_style='success')
record_manual_btn = widgets.Button(description='🎤 Record (Manual Stop)', button_style='info')
stop_btn = widgets.Button(description='🛑 Stop', button_style='danger')

record_fixed_btn.on_click(lambda x: record_fixed_duration(duration_slider.value))
record_manual_btn.on_click(lambda x: threading.Thread(target=record_with_stop).start())
stop_btn.on_click(stop_recording)

display(duration_slider, record_fixed_btn, record_manual_btn, stop_btn)