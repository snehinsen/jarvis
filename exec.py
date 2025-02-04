import subprocess

import speech_recognition as sr

import ffmpeg

import API

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
    subprocess.run(["./ffmpeg/win/bin/ffplay.exe", "-nodisp", "-autoexit", CONVERTED_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        userInput = (
            recognizer.recognize_wit(audio, key=API.WIT_API_KEY))
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
        exit()
    elif command == "" :
        pass
    else:
        response = API.query_ollama(command)
        print(response)
        speak(response)
