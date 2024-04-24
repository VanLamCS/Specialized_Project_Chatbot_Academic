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
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
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
        text = obj_content["choices"][0]["message"]["content"]
        logprobs = obj_content["choices"][0]["logprobs"]["content"]
        logprob_list = [logprob["logprob"] for logprob in logprobs]
        logprobs_avg = sum(logprob_list) / len(logprob_list)
        return {"text": text, "score": logprobs_avg}