import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _has_pyaudio():
    try:
        import pyaudio  # noqa: F401

        return True
    except Exception:
        return False


def _iter_python310_commands():
    seen = set()

    env_candidate = os.environ.get("VISION_PYTHON310")
    if env_candidate:
        command = (env_candidate,)
        seen.add(command)
        yield list(command)

    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        default_candidate = Path(local_appdata) / "Programs" / "Python" / "Python310" / "python.exe"
        command = (str(default_candidate),)
        if command not in seen:
            seen.add(command)
            yield [str(default_candidate)]

    py_launcher = shutil.which("py")
    if py_launcher:
        command = (py_launcher, "-3.10")
        if command not in seen:
            seen.add(command)
            yield [py_launcher, "-3.10"]

    python310 = shutil.which("python3.10")
    if python310:
        command = (python310,)
        if command not in seen:
            seen.add(command)
            yield [python310]


def _command_supports_pyaudio(command):
    try:
        check = subprocess.run(
            [*command, "-c", "import pyaudio"],
            capture_output=True,
            text=True,
            timeout=8,
        )
    except Exception:
        return False
    return check.returncode == 0


def _ensure_microphone_runtime():
    if _has_pyaudio():
        return

    if os.environ.get("VISION_RUNTIME_SWITCHED") == "1":
        print("[Vision] PyAudio is unavailable in this interpreter. Voice input will use keyboard fallback.")
        return

    script_path = str(Path(__file__).resolve())
    args = sys.argv[1:]

    for command in _iter_python310_commands():
        if not _command_supports_pyaudio(command):
            continue

        env = os.environ.copy()
        env["VISION_RUNTIME_SWITCHED"] = "1"
        command_label = " ".join(command)
        print(f"[Vision] Restarting with {command_label} for microphone support...")
        completed = subprocess.run([*command, script_path, *args], env=env)
        raise SystemExit(completed.returncode)

    print(
        "[Vision] PyAudio is missing for this Python runtime. "
        "Use Python 3.10 or install PyAudio to enable microphone listening."
    )


_ensure_microphone_runtime()

from config import JARVIS_NAME
from handlers.exit_handler import handle_exit
from handlers.greeting_handler import handle_greeting
from handlers.info_handler import handle_info
from handlers.learn_handler import learn_new_qa
from handlers.utility_handler import handle_utility
from intent.intent_detector import detect_intent
from knowledge.basic_qa import get_qa_answer
from speech.listener import listen_command
from speech.speaker import speak
from tasks.ai_chat import ai_reply
from tasks.system import handle_system


def start_jarvis():
    speak(f"Hello, I am {JARVIS_NAME}. How can I help you?")

    while True:
        command = listen_command()
        if not command:
            continue

        command = command.lower().strip()
        time.sleep(0.2)
        intent = detect_intent(command)

        if intent == "EXIT":
            speak(handle_exit())
            break

        if intent == "LEARN":
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

        qa_answer = get_qa_answer(command)
        if qa_answer:
            speak(qa_answer)
            continue

        if intent == "GREETING":
            speak(handle_greeting())
            continue

        if intent == "UTILITY":
            response = handle_utility(command)
            if response:
                speak(response)
            continue

        if intent == "SYSTEM":
            response = handle_system(command)
            if response:
                speak(response)
            continue

        if intent == "INFO":
            response = handle_info(command)
            if response:
                speak(response)
            else:
                speak("I am not trained for this topic yet.")
            continue

        speak(ai_reply(command))


if __name__ == "__main__":
    start_jarvis()
