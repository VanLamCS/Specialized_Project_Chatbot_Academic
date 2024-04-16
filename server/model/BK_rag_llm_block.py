"""*For llm*"""
from dotenv import load_dotenv
import os
load_dotenv()

LLM_API_SERVICE_URL = os.environ.get('LLM_API_SERVICE_URL')



from Rag_helper import Rag_helper
from LLm_api_service import LLm_api_service

class BK_rag_llm_block:
  def __init__(self, llm_api_service_url):
    self.llm_service = LLm_api_service(llm_api_service_url | LLM_API_SERVICE_URL)

  def generate(self, prompt):
      result = self.llm_service.generate_text(prompt)

      return {"output": result["text"], "score": result["score"]}