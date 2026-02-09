# knowledge/basic_qa.py

import json
import os

# ---------------------------
# Static predefined Q&A
# ---------------------------
qa_data = {
    # OS
    "os": "An Operating System is system software that manages hardware and software resources.",
    "what is os": "An Operating System is system software that manages hardware and software resources.",
    "what is operating system": "An Operating System manages computer hardware and software.",

    # Database
    "database": "A database is an organized collection of data that can be easily accessed, managed, and updated.",
    "what is database": "A database is an organized collection of data that can be easily accessed, managed, and updated.",
    "define database": "A database stores structured information electronically.",

    # AI
    "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
    "what is ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
    "define ai": "AI enables machines to think, learn, and make decisions.",

    # AIM
    "aim": "Aim refers to a goal or purpose.",
    "what is aim": "Aim means the objective or purpose you want to achieve."
}

# ---------------------------
# Aliases / normalization map
# ---------------------------
ALIASES = {
    "a i": "ai",
    "artificial intelligence": "ai",
    "db": "database",
    "operating system": "os"
}

# ---------------------------
# Learned Q&A file
# ---------------------------
LEARNED_QA_FILE = "knowledge/learned_qa.json"

# cache learned data (IMPORTANT FIX)
_LEARNED_CACHE = None


def normalize(text: str) -> str:
    text = text.lower().strip()

    fillers = ["please", "tell me", "can you", "explain", "define"]
    for f in fillers:
        text = text.replace(f, "").strip()

    for k, v in ALIASES.items():
        text = text.replace(k, v)

    return text


def load_learned_qa():
    global _LEARNED_CACHE

    if _LEARNED_CACHE is not None:
        return _LEARNED_CACHE

    if not os.path.exists(LEARNED_QA_FILE):
        _LEARNED_CACHE = {}
        return _LEARNED_CACHE

    with open(LEARNED_QA_FILE, "r", encoding="utf-8") as f:
        _LEARNED_CACHE = json.load(f)
        return _LEARNED_CACHE


def get_qa_answer(command: str):
    command = normalize(command)
    learned_data = load_learned_qa()

    # 1️⃣ Exact match (static)
    if command in qa_data:
        return qa_data[command]

    # 2️⃣ Exact match (learned)
    if command in learned_data:
        return learned_data[command]

    # 3️⃣ Partial match (static – SAFE)
    for question, answer in qa_data.items():
        if command.startswith(question) or question.startswith(command):
            return answer

    # 4️⃣ Partial match (learned – SAFE)
    for question, answer in learned_data.items():
        if command.startswith(question) or question.startswith(command):
            return answer

    return None
