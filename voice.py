import os
import uuid
import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# 🔐 Your Google Gemini 2.0 Flash API key
GOOGLE_API_KEY = "AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# 🎙️ Speech-to-Text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak your question:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 You asked: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ Request error: {e}")
    return None

# 🤖 Get Gemini 2.0 Flash response
def ask_gemini_flash(question):
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    try:
        print("📡 Asking Gemini 2.0 Flash...")
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data['candidates'][0]['content']['parts'][0]['text']
        return answer
    except Exception as e:
        print("❌ Error talking to Gemini Flash:")
        print(e)
        return "Sorry, I couldn't get an answer from Gemini."

# 🔈 Convert to speech + Save + Play
def speak_and_save(text, output_dir="voice_outputs"):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"response_{uuid.uuid4().hex[:8]}.mp3")
    tts = gTTS(text=text)
    tts.save(filename)
    print(f"💾 Audio saved: {filename}")
    print("🔊 Speaking...")
    playsound(filename)

# 🚀 Main Assistant
def run_voice_to_voice_assistant():
    print("🔁 Voice-to-Voice Assistant (Gemini 2.0 Flash)")
    question = recognize_speech()
    if not question:
        return
    answer = ask_gemini_flash(question)
    print(f"🤖 Gemini Answer: {answer}")
    speak_and_save(answer)

# 🏁 Run
if __name__ == "__main__":
    run_voice_to_voice_assistant()