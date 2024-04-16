import json
import requests # type: ignore

class LLm_api_service:
    def __init__(self, api_url):
        self.api_url = api_url

    def generate_text(self, user_input):
        body = {
            "inputs": f"<start_of_turn>user\n{user_input}\n<end_of_turn>\n<start_of_turn>model\n",
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

        return {"text":result, "score":log_prob_avg}
