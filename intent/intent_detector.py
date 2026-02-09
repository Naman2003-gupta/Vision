from intent.intent_map import INTENTS
import re

def detect_intent(command: str):
    command = command.lower().strip()

    # Split into clean words
    words = re.findall(r"\b\w+\b", command)

    for intent, keywords in INTENTS.items():
        for key in keywords:
            key = key.lower()

            # multi-word intent (e.g. "open chrome")
            if " " in key and key in command:
                return intent

            # single-word intent (exact match only)
            if key in words:
                return intent

    return "UNKNOWN"
