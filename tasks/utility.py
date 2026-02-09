from datetime import datetime
from config import JARVIS_NAME

def handle_utility(command):
    command = command.lower()

    if "time" in command:
        time_now = datetime.now().strftime("%H:%M")
        return f"The current time is {time_now}"

    if "date" in command:
        date_today = datetime.now().strftime("%d %B %Y")
        return f"Today's date is {date_today}"

    if "hello" in command or "hi" in command:
        return "Hello! I am ready and listening."

    if "how are you" in command:
        return "I am functioning perfectly. Thank you for asking."

    if "your name" in command:
        return f"My name is {JARVIS_NAME}"

    return None
