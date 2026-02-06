from speech.listener import listen_command
from speech.speaker import speak
from tasks.utility import handle_utility
from config import JARVIS_NAME
import time

def start_jarvis():
    speak(f"Hello, I am {JARVIS_NAME}. How can I help you?")

    while True:
        command = listen_command()

        if command == "":
            continue

        # Stop mic loop briefly before speaking
        time.sleep(0.2)

        handled = handle_utility(command)

        if not handled:
            speak("I heard you, but this command is not available yet.")

if __name__ == "__main__":
    start_jarvis()
