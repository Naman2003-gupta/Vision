import pyttsx3
import time


def speak(text):
    print("Jarvis:", text)

    # Re-initialize each call to avoid intermittent Windows TTS lockups.
    engine = pyttsx3.init("sapi5")

    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 165)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

    time.sleep(0.2)
