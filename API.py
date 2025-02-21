import requests
import json
import os
import re
from pyht import Client
from pyht.client import TTSOptions
from faster_whisper import WhisperModel

# API Configuration
URL = "http://localhost:3000/api"
LLM_API_KEY = ""
WIT_API_KEY = ""
MEMORY_FILE = "memory.json"

# Load API keys from file
with open("env.key", "r") as key_file:
    LLM_API_KEY = key_file.readline().strip()
    WIT_API_KEY = key_file.readline().strip()
    print(f"AI API KEY: {LLM_API_KEY}")
    print(f"WIT: {WIT_API_KEY}")

# Load or create memory file
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as mem_file:
        try:
            memory = json.load(mem_file)
        except json.JSONDecodeError:
            memory = []
else:
    memory = []

def save_memory():
    with open(MEMORY_FILE, "w") as memory_file:
        json.dump(memory, memory_file)

def extract_json(text):
    json_pattern = re.search(r'\{.*\}', text, re.DOTALL)
    if json_pattern:
        json_str = json_pattern.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None

def query_llm(message, error=False, retry_count=0, max_retries=3):
    if retry_count >= max_retries:
        print("❌ Maximum retry attempts reached. Aborting request.")
        return "I'm having trouble understanding. Please try again."

    memory.append({"role": "user", "content": message})
    save_memory()

    data = {"model": "jarvis:latest", "messages": memory}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LLM_API_KEY}"}

    try:
        print("Running...")
        response = requests.post(f"{URL}/chat/completions", json=data, headers=headers)
        response_json = response.json()
        print("Response received")

        if "choices" in response_json and response_json["choices"]:
            raw_response = response_json["choices"][0]["message"]["content"]
            print("🔹 JARVIS Raw Response:", raw_response)

            response_parsed = extract_json(raw_response)
            if not response_parsed:
                print("🚨 JSON Parsing Error. Retrying...")
                return query_llm("ERROR: Invalid JSON response!", error=True, retry_count=retry_count + 1)

            memory.append(
                {
                    "role": "assistant",
                    "content": f"{response_parsed}"
                }
            )
            save_memory()
            return response_parsed.get("message", "")
        else:
            return "JARVIS didn't respond properly."

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to LLM: {e}")
        return "My brain isn't working right now."

def get_tts_client():
    return Client(
        user_id="qhgqjWCZF2M3DckizpcckXerJQB3",
        api_key="f6359a724f964eceae9ef293eaab85d9"
    )

def get_tts_options():
    return TTSOptions(
        voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json"
    )

def tools():
    toolsList = os.listdir("./tools/")
    return toolsList

# Load Faster Whisper Model
model = WhisperModel("small", device="cpu", compute_type="int8")

def transcribe_audio(audio_file):
    segments, _ = model.transcribe(audio_file)
    return " ".join([segment.text for segment in segments])
