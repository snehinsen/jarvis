import requests
from pyht import Client
from pyht.client import TTSOptions

# API Configuration
URL = "http://tools.tlcp.com:3000/api" # CONNECTED BY LOCAL TWINGATE
LLM_API_KEY = ""
WIT_API_KEY = ""

# Load API keys from file
with open("env.key", "r") as key_file:
    LLM_API_KEY = key_file.readline().strip()
    WIT_API_KEY = key_file.readline().strip()
    print(f"AI API KEY: {LLM_API_KEY}")
    print(f"WIT: {WIT_API_KEY}")

def query_ollama(prompt):
    """Send prompt to OpenWebUI API and get response."""
    url = f"{URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Accept": "application/json"
    }
    data = {
        "model": "jarvis:latest",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "I didn't get a response from my AI module."
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to OpenWebUI: {e}")
        return "I couldn't connect to my AI module."

def get_tts_client():
    """Initialize TTS client."""
    return Client(
        user_id="qhgqjWCZF2M3DckizpcckXerJQB3",
        api_key="f6359a724f964eceae9ef293eaab85d9"
    )

def get_tts_options():
    """Get TTS options."""
    return TTSOptions(
        voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json"
    )
