import os
import uuid
import requests
from playsound import playsound

# 🔐 Your ElevenLabs API Key
ELEVEN_API_KEY = "sk_d57de3d2292d78ef63f64e7eae4aa514529065aedb81aa29"

# 🔈 Voice ID (Rachel by default)
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

# 📂 Output folder
OUTPUT_DIR = "elevenlabs_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🎤 Text-to-speech conversion function
def convert_text_to_speech(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7
        }
    }

    print("📡 Sending request to ElevenLabs API...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        filename = os.path.join(OUTPUT_DIR, f"speech_{uuid.uuid4().hex[:8]}.mp3")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Audio saved at: {filename}")

        print("🔊 Playing audio...")
        playsound(filename)
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.text)

# 🚀 App entry point
def run():
    print("🎙️ ElevenLabs Text-to-Speech Converter")
    user_text = input("📝 Enter text to convert to speech: ").strip()

    if not user_text:
        print("⚠️ No text provided.")
        return

    convert_text_to_speech(user_text)

# 🏁 Main
if __name__ == "__main__":
    run()
