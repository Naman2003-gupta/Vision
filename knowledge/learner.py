# knowledge/learner.py
import json
import os

LEARNED_FILE = "knowledge/learned_qa.json"

def load_learned_qa():
    if not os.path.exists(LEARNED_FILE):
        return {}

    with open(LEARNED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_learned_qa(data):
    with open(LEARNED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_new_qa(question, answer):
    data = load_learned_qa()
    data[question.lower()] = answer
    save_learned_qa(data)

def get_learned_answer(command):
    data = load_learned_qa()
    return data.get(command.lower())
