import requests
import os
from PIL import Image
from io import BytesIO

# 🔐 Replace with your actual Stability AI API key
api_key = "sk-OcW1iVsEEQNSOoMw550u1ht2hlbg5Nu4zIeyktz2rup1LWf4"

# 🌐 Stability AI v2beta endpoint
url = "https://api.stability.ai/v2beta/stable-image/generate/core"

# 📝 Prompt from user
prompt = input("🎨 Enter your image prompt: ")

# 🧾 Headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "image/*"  # Required for image response
}

# 📤 multipart/form-data payload
files = {
    "prompt": (None, prompt),
    "output_format": (None, "png"),
    "aspect_ratio": (None, "1:1"),
    "mode": (None, "text-to-image")
}

# 🚀 Send request to Stability API
response = requests.post(url, headers=headers, files=files)

# 💾 Handle and display result
if response.status_code == 200:
    image_bytes = BytesIO(response.content)

    # Save the image
    image_path = "generated_image.png"
    with open(image_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Image saved as {image_path}")

    # 📸 Display the image using PIL
    try:
        image = Image.open(image_bytes)
        image.show()  # Opens the image in default viewer
        print("🖼️ Image opened in default viewer.")
    except Exception as e:
        print("⚠️ Could not open image:", e)
else:
    print(f"❌ Error {response.status_code}")
    print("Response:", response.text)