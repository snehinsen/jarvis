import subprocess

from gtts import gTTS
import pyttsx3
import speech_recognition as sr
from ibm_watsonx_ai.libs.ibmfl.party_env_validator import stderr

import API


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        userInput = (
            recognizer.recognize_wit(audio, key=API.WIT_API_KEY))
        print(f"You said: {userInput}")
        return userInput
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Speech recognition service is down.")
        return ""


def nspeak(text: str):
    pyttsx3.speak(text)


def fspeak(text):
    FILE_NAME = "output.mp3"
    tts = gTTS(text)
    tts.save(FILE_NAME)

    print("Playing response...")

    # Play audio using ffmpeg's ffplay
    (subprocess
    .run(
        [
            "ffplay",
            "-nodisp",
            "-autoexit",
            FILE_NAME
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ))
