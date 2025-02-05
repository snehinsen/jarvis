import subprocess
import openwakeword.utils
import pyaudio
import pyttsx3
import speech_recognition as sr
import numpy as np

from openwakeword.model import Model

openwakeword.utils.download_models()

import API

FILE_NAME = "output.mp3"

# Microphone Stream Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280  # Small chunk size for real-time detection

# Initialize PyAudio for microphone input
audioDriver = pyaudio.PyAudio()
mic_stream = (
    audioDriver.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
)

wake_word = "hey jarvis"
model = Model(
    [
        wake_word.replace(" ", "_"),
    ],
    inference_framework="onnx"
)


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        userInput = recognizer.recognize_wit(audio, key=API.WIT_API_KEY)
        print(f"You said: {userInput}")
        return userInput
    except sr.UnknownValueError:
        print("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        print("Speech recognition service is down.")
        return ""


while True:
    if listen().lower() == "hay jarvis":  # Adjust threshold as needed
        while True:
            command = listen()
            if "exit" in command.lower():
                pyttsx3.speak("Goodbye!")
                break
            elif command:
                response = API.query_ollama(command)
                print(response)
                pyttsx3.speak(response)
