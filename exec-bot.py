import subprocess
import openwakeword.utils
import pyaudio
import pyttsx3
from openwakeword.model import Model

openwakeword.utils.download_models()

import API
from audio import listen

FILE_NAME = "output.mp3"

# Microphone Stream Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280

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

def on_start():
    while True:
        # Listen for the wake word (exact match)
        command = listen().lower()  # Assuming listen() is already handling speech recognition

        if command == wake_word.lower():  # Exact match for "hey jarvis"
            print("Wake Word Detected")
            while True:
                command = listen()
                if "exit" in command.lower():  # Allow for an exit command
                    break
                elif command:
                    response = API.query_ollama(command)
                    print(response)
                    pyttsx3.speak(response)
        elif command.lower() == "shut down jarvis":
            exit()

on_start()