import subprocess

import pyttsx3
import speech_recognition as sr

import API

FILE_NAME = "output.mp3"

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
    if "exit" in command.lower():
        pyttsx3.speak("Goodbye!")
        exit()
    elif command == "" :
        pass
    else:
        response = API.query_ollama(command)
        print(response)
        pyttsx3.speak(response)
