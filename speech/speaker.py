import pyttsx3
import time

def speak(text):
    print("🤖 Jarvis:", text)

    # 🔥 Re-initialize engine EVERY time (Windows fix)
    engine = pyttsx3.init("sapi5")

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # 1 for female
    engine.setProperty("rate", 165)
    
#  engine = pyttsx3.init("sapi5")
#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[0].id)
#     engine.setProperty("rate", 165)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

    time.sleep(0.2)
