import requests
from PIL import Image
from io import BytesIO

# ✅ Hugging Face API Key (Replace with yours)
HF_API_KEY = "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"

# 🌐 Model endpoint
HF_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# ✅ Function to send request and get image bytes
def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",  # ✅ Correct header
        "Content-Type": "application/json",
        "Accept": "image/png"
    }

    payload = {
        "inputs": prompt
    }

    print("🚀 Sending request to Hugging Face API...")
    response = requests.post(HF_MODEL_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        print(f"❌ Failed with status {response.status_code}")
        print("Response:", response.text)
        return None

# ✅ Function to save and show the image
def save_and_show_image(image_bytes, filename="generated_image.png"):
    with open(filename, "wb") as f:
        f.write(image_bytes)
    print(f"✅ Image saved as {filename}")

    try:
        image = Image.open(BytesIO(image_bytes))
        image.show()
        print("🖼️ Image displayed.")
    except Exception as e:
        print("⚠️ Could not display image:", e)

# ✅ Main function
def main():
    prompt = input("🎨 Enter your image prompt: ").strip()
    image_bytes = generate_image(prompt)

    if image_bytes:
        save_and_show_image(image_bytes)

if __name__ == "__main__":
    main()