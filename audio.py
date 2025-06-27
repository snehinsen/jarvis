import pyttsx3
import speech_recognition as sr
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

def nspeak(message: str):
    pyttsx3.speak(message)

def fspeak(text):
    FILE_NAME = "output.mp3"
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
