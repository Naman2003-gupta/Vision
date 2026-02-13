# test_voice.py
import pyttsx3
engine = pyttsx3.init("sapi5")
engine.say("Vision voice test successful")
engine.runAndWait()
