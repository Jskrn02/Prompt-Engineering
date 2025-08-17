import os
import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor
from scipy.io.wavfile import write

# ======== Configuration ========
MODEL_NAME = "facebook/musicgen-small"  # You can also try 'musicgen-medium'
OUTPUT_DIR = "generated_music"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======== Load Model and Processor ========
print("🔄 Loading MusicGen model...")
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = MusicgenForConditionalGeneration.from_pretrained(MODEL_NAME)

# Optional: Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# ======== Input Prompt ========
prompt = input("🎶 Enter music description (e.g., 'Happy lo-fi beat with piano and rain sounds'): ")

# ======== Preprocess and Generate ========
inputs = processor(
    text=[prompt],
    padding=True,
    return_tensors="pt"
).to(device)

print("🎼 Generating music... This may take 30–60 seconds.")
audio_values = model.generate(**inputs, max_new_tokens=1024)

# ======== Save Output ========
sample_rate = model.config.audio_encoder.sampling_rate
output_path = os.path.join(OUTPUT_DIR, "musicgen_output.wav")

write(output_path, rate=sample_rate, data=audio_values[0, 0].cpu().numpy())

print(f"✅ Music saved to: {output_path}")