import requests
import json
import os
import re

from faster_whisper import WhisperModel
# from pyht import Client
# from pyht.client import TTSOptions

from audio import fspeak, nspeak
from run_module import launch as launch_tool
import dotenv

dotenv.load_dotenv()

URL = dotenv.get_key(dotenv_path=".env", key_to_get="LLM_API_URL")
LLM_API_KEY = dotenv.get_key(dotenv_path=".env", key_to_get="LLM_API_KEY")
WIT_API_KEY = dotenv.get_key(dotenv_path=".env", key_to_get="WIT_API_KEY")
MEMORY_FILE = "memory.json"
memory = []
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as mem_file:
        try:
            memory = json.load(mem_file)
        except json.JSONDecodeError:
            memory = []
else:
    memory = []

toolsList = []


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


def get_enabled_tools():
    enabled_tools = []
    tools_dir = "./tools"

    if not os.path.exists(tools_dir):
        print("⚠️ Tools directory does not exist.")
        return enabled_tools

    for item in os.listdir(tools_dir):
        tool_path = os.path.join(tools_dir, item)
        manifest_path = os.path.join(tool_path, "manifest.json")

        if os.path.isdir(tool_path) and os.path.isfile(manifest_path):
            try:
                with open(manifest_path, "r") as manifest_file:
                    manifest = json.load(manifest_file)
                    if manifest.get("enabled", False):
                        enabled_tools.append({
                            "id": item,
                            "manifest": manifest
                        })
            except json.JSONDecodeError:
                print(f"🚫 Failed to parse manifest for {item}")
            except Exception as e:
                print(f"❌ Error reading manifest for {item}: {e}")

    return enabled_tools


def query_llm(message, error=False, retry_count=0, max_retries=3, speak_type=1):
    global toolsList
    speak = fspeak if speak_type == 1 else nspeak
    if retry_count >= max_retries:
        speak("I'm having trouble understanding. Please try again.")
        return

    memory.append(
        {
            "role": "user",
            "content": str({
                "content": message,
                "from": "system" if error | message.__contains__("(From tool") else "user",
                "profile": {
                    "name": "sys-profiler" if error | message.__contains__("(From tool") else "Snehin Sen",
                    "gender": "" if error | message.__contains__("(From tool") else "male",
                    "role": "system-execute" if error | message.__contains__("(From tool") else "admin/user-client",
                },
                "available-tools-by-id": get_enabled_tools()
            })
        }
    )

    save_memory()

    data = {"model": "jarvis", "messages": memory}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LLM_API_KEY}"}

    try:
        response = requests.post(f"{URL}/chat/completions", json=data, headers=headers).json()
        print(response)
        if "choices" in response and response["choices"]:
            raw_response = response["choices"][0]["message"]["content"]
            print("🔹 JARVIS Raw Response:", raw_response)

            response_parsed = extract_json(raw_response)
            if not response_parsed:
                print("🚨 JSON Parsing Error. Retrying...")
                query_llm("ERROR: Invalid JSON response!",
                          error=True,
                          retry_count=retry_count + 1,
                          speak_type=speak_type)
            memory.append(
                {
                    "role": "assistant",
                    "content": f"{response_parsed}"
                }
            )
            save_memory()
            speak(response_parsed.get("message", ""))
            if response_parsed.get("tools"):
                print("🔧 Tools detected in response.")
                toolsList = response_parsed.get("tools")
                for tool in toolsList:
                    tool_vars_all = response_parsed.get("toolVars", {})
                    toolArgs = tool_vars_all.get(tool, {})
                    exec_result = launch_tool(tool, toolArgs)
                    print(exec_result)
                    query_llm(str(f"(From tool:{tool})\n{exec_result}"), speak_type=speak_type)
        else:
            nspeak("System didn't respond properly.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to LLM: {e}")
        speak("My brain isn't working right now.")


# def get_tts_client():
#     return Client(
#         user_id="qhgqjWCZF2M3DckizpcckXerJQB3",
#         api_key="ak-1a4dcf00071d495f921b5b0f51341b95"
#     )
#
# #
# # def get_tts_options():
# #     return TTSOptions(
# #         voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json"
# #     )
#

model = WhisperModel("small", device="cpu", compute_type="int8")


def transcribe_audio(audio_file):
    segments, _ = model.transcribe(audio_file)
    return " ".join([segment.text for segment in segments])
