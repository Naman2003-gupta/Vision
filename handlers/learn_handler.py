# handlers/learn_handler.py

import json
import os
from knowledge.basic_qa import normalize, LEARNED_QA_FILE


def learn_new_qa(question: str, answer: str):
    question = normalize(question)
    answer = answer.strip()

    data = {}

    if os.path.exists(LEARNED_QA_FILE):
        with open(LEARNED_QA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    data[question] = answer

    with open(LEARNED_QA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return "Got it. I have learned this."
