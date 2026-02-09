import speech_recognition as sr

def listen_command():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("🗣 You said:", command)
        return command.lower()
    except:
        return ""
