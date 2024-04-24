from . import chat_core

def create_answer(query):
    answers = chat_core.invoke(query)
    answer = "Chúng tôi thật sự xin lỗi vì không có câu trả lời phù hợp cho câu hỏi của bạn."
    score = float('-inf')
    for ans in answers:
        if ans["score"] > score:
            answer = ans["output"]
            score = ans["score"]
    print("\n\n==========CHECK ANSWERS==========\n\n", answers)
    return answer, score