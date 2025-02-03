import json
import subprocess
import requests
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import API

# Ensure dependencies are installed
subprocess.run(["pip", "install", "SpeechRecognition", "pydub", "requests", "pyaudio", "numpy", "sounddevice", "pyht"])
subprocess.run(["pip", "install", "ffmpeg-python"])  # Ensure ffmpeg is installed

FILE_NAME = "output.mp3"

def speak(text):
    """Convert text to speech and play it."""
    client = API.get_tts_client()
    options = API.get_tts_options()

    with open(FILE_NAME, "wb") as audio_file:
        for chunk in client.tts(text=text, options=options, voice_engine='PlayDialog-https'):
            audio_file.write(chunk)

    print("Playing response...")
    audio = AudioSegment.from_file(FILE_NAME, format="mp3")  # Convert if needed
    play(audio)  # Proper playback function

def listen():
    """Convert speech to text using Wit.ai (API key required)."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        userInput = recognizer.recognize_wit(audio, key=API.WIT_AI_KEY)
        print(f"You said: {userInput}")
        return userInput
    except sr.UnknownValueError:
        print("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        print("Speech recognition service is down.")
        return ""

# Main loop
while True:
    command = listen()
    if "exit" in command:
        speak("Goodbye!")
        break
    elif command:
        response = API.query_ollama(command)
        speak(response)
