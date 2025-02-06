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