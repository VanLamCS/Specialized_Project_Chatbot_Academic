import json
import requests # type: ignore
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL")

class LLm_api_service:
    def __init__(self, api_url):
        self.api_url = api_url

    def generate_text(self, user_input):
        body = {
            "inputs": f"<start_of_turn>user\n{user_input}\n<end_of_turn>\n<start_of_turn>model\n",
            "parameters": {
                "max_new_tokens": 700,
                "min_new_tokens": 250,
            },
            "model": "",
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.api_url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None, None

        result = ""
        log_prob_map = []

        if response.headers['Content-Type'] == 'text/event-stream':
            for line in response.iter_lines():
                if not line or line.decode('utf-8').startswith('#'):
                    continue

                line = line.decode('utf-8')
                data_str = line[5:]
                data_obj = json.loads(data_str)
                if 'token' in data_obj:
                    log_prob_map.append(data_obj['token']['logprob'])
                if data_obj['generated_text'] is not None:
                    result = data_obj['generated_text']
        else:
            print("Unexpected response content type:", response.headers['Content-Type'])

        if log_prob_map:
            log_prob_avg = sum(log_prob_map) / len(log_prob_map)
        else:
            log_prob_avg = None
        combined_score = log_prob_avg

        return {"text": result, "score": combined_score, "log_prob_map": log_prob_map}

    def openai_generate_text(self, prompt):
        body = {
            "model": "gpt-3.5-turbo",
            "logprobs": True,
            "n": 2,
            "messages": [
                {
                    "role": "system",
                    "content": "Bạn là một trợ lý để hỗ trợ sinh ra câu trả lời với ngữ cảnh và câu hỏi được cung cấp bởi người dùng. Trong đó tiền tố cho ngữ cảnh là: \"===Ngữ cảnh===:\". Tiền tố của câu hỏi là: \"===Câu hỏi===:\".\n Câu trả lời sẽ được sinh ra dựa vào nội dung của ngữ cảnh mà không được lấy thông tin ở bất kỳ nguồn nào khác. Nếu không sinh ra được câu trả lời từ ngữ cảnh hãy phản hồi \"Tôi không có câu trả lời cho câu hỏi này, hãy đặt lại câu hỏi với đầy đủ thông tin hơn.\"."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + OPENAI_API_KEY,
        }
        try:
            response = requests.post(OPENAI_API_URL + "/v1/chat/completions", data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None, None
        str_content = response.content.decode("utf-8")
        obj_content = json.loads(str_content)

        logprobs_avg_max = float('-inf')
        text = ""
        for choice in obj_content["choices"]:
            logprobs = choice["logprobs"]["content"]
            logprob_list = [logprob["logprob"] for logprob in logprobs]
            logprobs_avg = sum(logprob_list) / len(logprob_list)
            if logprobs_avg_max < logprobs_avg:
                text = choice["message"]["content"]
                logprobs_avg_max = logprobs_avg

        return {"text": text, "score": logprobs_avg_max}