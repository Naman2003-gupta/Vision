from speech.listener import listen_command
from speech.speaker import speak
from intent.intent_detector import detect_intent

from handlers.greeting_handler import handle_greeting
from handlers.exit_handler import handle_exit
from handlers.info_handler import handle_info
from handlers.utility_handler import handle_utility
from handlers.learn_handler import learn_new_qa

from tasks.system import handle_system
from tasks.ai_chat import ai_reply

from knowledge.basic_qa import get_qa_answer
from config import JARVIS_NAME

import time


def start_jarvis():
    speak(f"Hello, I am {JARVIS_NAME}. How can I help you?")

    while True:
        command = listen_command()

        if not command:
            continue

        command = command.lower().strip()
        time.sleep(0.2)

        # 1️⃣ Detect intent FIRST
        intent = detect_intent(command)

        # 2️⃣ EXIT (highest priority)
        if intent == "EXIT":
            speak(handle_exit())
            break

        # 3️⃣ LEARN MODE 🔥
        elif intent == "LEARN":
            speak("Okay. What is the question?")
            question = listen_command()

            if not question:
                speak("I did not hear the question.")
                continue

            speak("What is the answer?")
            answer = listen_command()

            if not answer:
                speak("I did not hear the answer.")
                continue

            response = learn_new_qa(question, answer)
            speak(response)
            continue

        # 4️⃣ Knowledge Base (static + learned Q&A)
        qa_answer = get_qa_answer(command)
        if qa_answer:
            speak(qa_answer)
            continue

        # 5️⃣ Greeting
        elif intent == "GREETING":
            speak(handle_greeting())

        # 6️⃣ Utility
        elif intent == "UTILITY":
            response = handle_utility(command)
            if response:
                speak(response)

        # 7️⃣ System commands
        elif intent == "SYSTEM":
            response = handle_system(command)
            if response:
                speak(response)

        # 8️⃣ Info handler
        elif intent == "INFO":
            response = handle_info(command)
            if response:
                speak(response)
            else:
                speak("I am not trained for this topic yet.")

        # 9️⃣ AI fallback (LAST option)
        else:
            speak(ai_reply(command))


if __name__ == "__main__":
    start_jarvis()
