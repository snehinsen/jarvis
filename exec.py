import json
import subprocess
from logging import ERROR

import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment
import API

# Ensure dependencies are installed
subprocess.run(["pip", "install", "SpeechRecognition", "pydub", "requests", "pyaudio", "numpy", "sounddevice", "pyht"])
subprocess.run(["pip", "install", "ffmpeg-python"])  # Ensure ffmpeg is installed

FILE_NAME = "output.mp3"
CONVERTED_FILE = "output.wav"  # If needed

def speak(text):
    """Convert text to speech and play it using ffmpeg."""
    client = API.get_tts_client()
    options = API.get_tts_options()

    with open(FILE_NAME, "wb") as audio_file:
        for chunk in client.tts(text=text, options=options, voice_engine='PlayDialog-https'):
            audio_file.write(chunk)

    print("Playing response...")

    # Convert MP3 to WAV using ffmpeg (optional)
    ffmpeg.input(FILE_NAME).output(CONVERTED_FILE).run(overwrite_output=True)

    # Play audio using ffmpeg's ffplay
    subprocess.run(["ffplay", "-nodisp", "-autoexit", CONVERTED_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
try:
    while True:
        command = listen()
        if "exit" in command:
            speak("Goodbye!")
            exit()
        else:
            response = API.query_ollama(command)
            speak(response)
except Exception:
    print("ERROR")