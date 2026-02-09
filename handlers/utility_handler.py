import datetime

def handle_utility(command):
    if "time" in command:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M')}"
    if "date" in command:
        return f"Today's date is {datetime.datetime.now().strftime('%d %B %Y')}"
    return None
