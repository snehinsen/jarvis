import subprocess

import speech_recognition as sr

import ffmpeg

import API
from audio import listen

FILE_NAME = "output.mp3"


def speak(text):
    client = API.get_tts_client()
    options = API.get_tts_options()

    with open(FILE_NAME, "wb") as audio_file:
        for chunk in client.tts(
                text=text,
                options=options,
                voice_engine='PlayDialog-http'):
            audio_file.write(chunk)

    print("Playing response...")

    # Play audio using ffmpeg's ffplay
    (subprocess
        .run(
            [
                "./ffmpeg/win/bin/ffplay.exe",
                "-nodisp",
                "-autoexit",
                FILE_NAME
            ],
            stdout=subprocess.DEVNULL
        )
    )


while True:
    command = listen()
    if "exit" in command:
        speak("Goodbye!")
        exit()
    elif command == "":
        pass
    else:
        response = API.query_ollama(command)
        print(response)
        speak(response)
