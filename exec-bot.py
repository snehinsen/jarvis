import pyaudio
from openwakeword.model import Model
import API
from audio import listen, nspeak

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


def on_start():
    while True:
        command = listen().lower()

        if command == wake_word.lower():
            nspeak("Yes sir?")
            while True:
                command = listen()
                if "exit" in command.lower():  # Allow for an exit command
                    break
                elif command:
                    API.query_llm(command, speak_type=2)
        elif command == "shut down jarvis":
            exit()
on_start()