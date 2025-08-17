import tkinter as tk
import sounddevice as sd
import numpy as np
import wave
import datetime
import speech_recognition as sr
import threading
import os

# ---------- Configuration ----------
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = 'int16'

# ---------- File Utilities ----------
def get_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def get_audio_filename():
    return f"audio_{get_timestamp()}.wav"

def get_text_filename(audio_filename):
    return audio_filename.replace(".wav", ".txt")

def save_audio_file(filename, data, samplerate):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # int16
        wf.setframerate(samplerate)
        wf.writeframes(data.tobytes())
    print(f"✅ Saved audio to {filename}")

# ---------- Transcription ----------
def transcribe_audio_google(filename, output_widget=None):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print(f"📝 Transcription: {text}")

            # Save to file
            txt_file = get_text_filename(filename)
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(text)

            # Update GUI
            if output_widget:
                output_widget.delete("1.0", tk.END)
                output_widget.insert(tk.END, text)

            print(f"✅ Saved transcription to {txt_file}")
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
        if output_widget:
            output_widget.insert(tk.END, "Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ API request failed: {e}")
        if output_widget:
            output_widget.insert(tk.END, f"API request error: {e}")

# ---------- Fixed Duration Record ----------
def record_fixed_duration(duration=5, output_widget=None):
    def task():
        filename = get_audio_filename()
        print(f"🎤 Recording for {duration} seconds...")
        recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                           channels=CHANNELS, dtype=DTYPE)
        sd.wait()
        save_audio_file(filename, recording, SAMPLE_RATE)
        transcribe_audio_google(filename, output_widget)

    threading.Thread(target=task).start()

# ---------- Manual Start/Stop Recording ----------
is_recording = False
recorded_chunks = []

def start_manual_recording(stop_btn, output_widget=None):
    global is_recording, recorded_chunks
    is_recording = True
    recorded_chunks = []

    def callback(indata, frames, time, status):
        if is_recording:
            recorded_chunks.append(indata.copy())

    stream = sd.InputStream(callback=callback, channels=CHANNELS,
                            samplerate=SAMPLE_RATE, dtype=DTYPE)
    stream.start()
    stop_btn.config(state=tk.NORMAL)

    def monitor():
        while is_recording:
            sd.sleep(100)
        stream.stop()
        stream.close()
        audio_data = np.concatenate(recorded_chunks, axis=0)
        filename = get_audio_filename()
        save_audio_file(filename, audio_data, SAMPLE_RATE)
        transcribe_audio_google(filename, output_widget)

    threading.Thread(target=monitor).start()

def stop_manual_recording(stop_btn):
    global is_recording
    is_recording = False
    stop_btn.config(state=tk.DISABLED)
    print("🛑 Manual recording stopped.")

# ---------- GUI ----------
def build_gui():
    root = tk.Tk()
    root.title("🎙️ Google Speech-to-Text App")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    # --- Fixed Duration ---
    tk.Label(frame, text="🎧 Record Fixed Duration (5 seconds)").pack(pady=5)
    tk.Button(frame, text="Record 5 Seconds",
              command=lambda: record_fixed_duration(5, output_text)).pack(pady=5)

    # --- Manual Record ---
    tk.Label(frame, text="🎧 Manual Start/Stop Recording").pack(pady=5)
    tk.Button(frame, text="Start Recording",
              command=lambda: start_manual_recording(stop_button, output_text)).pack(pady=5)
    global stop_button
    stop_button = tk.Button(frame, text="Stop Recording",
                            command=lambda: stop_manual_recording(stop_button),
                            state=tk.DISABLED)
    stop_button.pack(pady=5)

    # --- Transcription Output ---
    tk.Label(frame, text="📝 Transcription Output").pack(pady=5)
    global output_text
    output_text = tk.Text(frame, height=10, width=60, wrap=tk.WORD)
    output_text.pack(pady=10)

    root.mainloop()

# ---------- Run the App ----------
if __name__ == "__main__":
    build_gui()