import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import time
import os
import sys

# 🔐 Your Gemini 2.0 Flash API key
GOOGLE_API_KEY = "AIzaSyAkxBGTwBGWn9vqnPdqbT7L4MWHv2Wa_p4"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# 📥 Fetch and parse website content
def fetch_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ')
        markdown = md(str(soup.body))
        return text, markdown, soup
    except Exception as e:
        print(f"❌ Error fetching content: {e}")
        return "", "", None

# 🧠 Generate summary using Gemini 2.0 Flash
def summarize_with_gemini(text):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": f"Summarize the following website content in well-structured markdown format:\n\n{text}"
            }]
        }]
    }
    response = requests.post(f"{GEMINI_API_URL}?key={GOOGLE_API_KEY}", headers=headers, json=data)
    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        print("❌ Gemini API Error:", response.json())
        return "Summary could not be generated."

# 💾 Save text to file
def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 🔄 Reframe the summary text
def reframe_summary(summary):
    # Simple rewording logic
    return summary.replace("In summary,", "To wrap things up,").replace("Overall,", "In conclusion,")

# 🔗 Extract internal and external links
def extract_links(soup, base_url):
    internal, external = set(), set()
    domain = base_url.split("//")[-1].split("/")[0]
    if not soup:
        return [], []

    for tag in soup.find_all('a', href=True):
        href = tag['href']
        if href.startswith('/'):
            internal.add(base_url.rstrip('/') + href)
        elif domain in href:
            internal.add(href)
        elif href.startswith("http"):
            external.add(href)
    return list(internal), list(external)

# 🎞️ ChatGPT-style typewriter effect (word by word)
def typewriter(text, delay=0.01, pause_on_punctuation=True):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if pause_on_punctuation and char in ".!?":
            time.sleep(delay * 10)  # Longer pause after sentence
        else:
            time.sleep(delay * 2)
    print("\n")

# 🚀 Main program
def main():
    url = input("🌐 Enter website URL to summarize: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    print("\n📡 Fetching website content...")
    raw_text, markdown, soup = fetch_website_content(url)

    print("🤖 Summarizing using Gemini 2.0 Flash...")
    summary = summarize_with_gemini(raw_text)

    os.makedirs("summaries", exist_ok=True)
    original_file = "summaries/original_summary.md"
    reframed_file = "summaries/reframed_summary.md"

    save_to_file(summary, original_file)

    reframed = reframe_summary(summary)
    save_to_file(reframed, reframed_file)

    internal_links, external_links = extract_links(soup, url)

    print("\n📝 Original Summary (ChatGPT-style Output):\n")
    typewriter(summary)

    print("\n📝 Reframed Summary (ChatGPT-style Output):\n")
    typewriter(reframed)

    print("\n🔗 Internal Links Found:")
    for link in internal_links:
        print(" -", link)

    print("\n🌍 External Links Found:")
    for link in external_links:
        print(" -", link)

if __name__ == "__main__":
    main()