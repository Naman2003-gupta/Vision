import datetime
from speech.speaker import speak

def handle_utility(command):
    if "time" in command:
        speak("Sure. Let me check the time.")
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {time}")
        return True

    elif "date" in command:
        speak("Okay. Fetching today's date.")
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")
        return True

    elif "hello" in command or "hi" in command:
        speak("Hello! I am ready and listening.")
        return True

    elif "how are you" in command:
        speak("I am functioning perfectly. Thank you for asking.")
        return True

    elif "exit" in command or "stop" in command:
        speak("Shutting down. Have a nice day.")
        exit()

    return False
