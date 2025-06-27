from openwakeword.model import Model
import API
from audio import listen, fspeak

wake_word = "hey jarvis"

model = Model(
    [
        wake_word.replace(" ", "_"),
    ],
    inference_framework="onnx"
)


def on_start():
    while True:
        command = listen().lower()

        if command == wake_word.lower():
            fspeak("Yes Sir!")
            while True:
                command = listen()
                if "exit" in command.lower():
                    exit()
                elif command:
                    API.query_llm(command)
        elif command == "shut down jarvis":
            exit()

on_start()
