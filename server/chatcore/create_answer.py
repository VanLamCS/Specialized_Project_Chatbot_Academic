from . import chat_core

def create_answer(query):
    answers = chat_core.invoke(query)
    answer = ""
    score = -1
    for a in answers:
        if a["score"] > score:
            answer = a["output"]
    return answer, score