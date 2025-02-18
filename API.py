import requests
import json
from pyht import Client
from pyht.client import TTSOptions
import os


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


def query_llm(prompt):
    memory.extend(memory)
    memory.append({"role": "user", "content": prompt})

    data = {
        "model": "jarvis:latest",
        "messages": memory
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}"
    }

    try:
        response = requests.post(f"{URL}/chat/completions", json=data, headers=headers)
        response_json = response.json()

        if "choices" in response_json and response_json["choices"]:
            raw_response = response_json["choices"][0]["message"]["content"]
            print("🔹 JARVIS Raw Response:", raw_response)

            try:
                print(f"Raw Response: {raw_response}")
                response_parsed = json.loads(raw_response)
            except json.JSONDecodeError as e:
                print("🚨 JSON Parsing Error:", e)
                return "Oops! JARVIS sent an invalid response."

            tools_list = response_parsed.get("tools", [])
            ai_response = response_parsed.get("message", "")

            print("✅ Parsed Tools:", tools_list)
            print("✅ Parsed Message:", ai_response)

            memory.append({"role": "assistant", "content": ai_response})
            save_memory()
            return ai_response
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
