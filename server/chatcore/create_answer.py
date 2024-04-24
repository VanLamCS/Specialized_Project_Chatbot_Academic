from . import chat_core

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):].strip()
    return text

def remove_answer_prefix(answer, arr_prefix = []):
    cleaned_answer = answer
    for prefix in arr_prefix:
        cleaned_answer = remove_prefix(cleaned_answer, prefix)
    return cleaned_answer

def evaluate_relevance(answer, question):
    answer_tokens = set(answer.lower().split())
    question_tokens = set(question.lower().split())
    common_tokens = answer_tokens.intersection(question_tokens)
    relevance_score = len(common_tokens) / len(question_tokens)
    return relevance_score

def total_score(answer, question, base_score):
    relevance_score = evaluate_relevance(answer, question)
    return base_score + relevance_score * 1.0

def create_answer(query):
    answers, docs_merged = chat_core.invoke(query)
    answer = "Chúng tôi thật sự xin lỗi vì không có câu trả lời phù hợp cho câu hỏi của bạn."
    score = float('-inf')
    # for a in answers:
    #     a["score"] = total_score(a["output"], query, a["score"])
    for a in answers:
        if a["score"] > score:
            answer = a["output"]
            score = a["score"]
    return remove_answer_prefix(answer, ["**Phản hồi:**", "**Phản hồi**", "**Phản hồi hoàn thành yêu cầu**"]), score, answers