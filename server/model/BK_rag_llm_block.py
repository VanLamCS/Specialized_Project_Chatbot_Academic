"""*For llm*"""
import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_SERVICE_URL = os.getenv('LLM_API_SERVICE_URL')

from model.LLm_api_service import LLm_api_service

class BK_rag_llm_block:
  def __init__(self, llm_api_service_url):
    self.llm_service = LLm_api_service(llm_api_service_url or LLM_API_SERVICE_URL)

  def generate(self, prompt):
      result = self.llm_service.generate_text(prompt)
      # print("prompt: ", prompt,
      #       "\noutput: ", result["text"],
      #       "\nscore: ", result["score"],
      #       "\nlog_prob_map: ", result["log_prob_map"],
      #       '\n------------------------------------------------------------\n')


      return {"output": result["text"], "score": result["score"]}