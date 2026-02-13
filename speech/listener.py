import sys

import speech_recognition as sr

_warned_no_mic = False


def _typed_fallback():
    try:
        return input("Type command: ").strip().lower()
    except EOFError:
        return ""


def _build_mic_hint(exc):
    message = str(exc)
    if "PyAudio" not in message:
        return ""

    return (
        "PyAudio is not available in this Python runtime. "
        "Run Vision with Python 3.10 (for example: `py -3.10 main.py`) "
        f"or install PyAudio for Python {sys.version_info.major}.{sys.version_info.minor}."
    )


def listen_command():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    except (AttributeError, OSError) as exc:
        global _warned_no_mic
        if not _warned_no_mic:
            print(f"Microphone unavailable ({exc}). Falling back to keyboard input.")
            hint = _build_mic_hint(exc)
            if hint:
                print(hint)
            _warned_no_mic = True
        return _typed_fallback()
    except sr.WaitTimeoutError:
        return ""
    except Exception as exc:
        print(f"Audio input error: {exc}")
        return ""

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower().strip()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as exc:
        print(f"Speech recognition service error: {exc}")
        return ""
