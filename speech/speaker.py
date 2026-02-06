import pyttsx3

engine = pyttsx3.init('sapi5')   # IMPORTANT for Windows

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
engine.setProperty('rate', 170)             # speaking speed
engine.setProperty('volume', 1.0)           # max volume

def speak(text):
    print(f"🤖 Jarvis: {text}")  # console confirmation
    engine.say(text)
    engine.runAndWait()
