"""# **Constants**"""
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL_ID = os.getenv('EMBEDDING_MODEL_ID')
DOCS_PATH = os.getenv('DOCS_PATH')
MAX_NEW_TOKENS = os.getenv('MAX_NEW_TOKENS')
LLM_API_SERVICE_URL = os.getenv('LLM_API_SERVICE_URL')
DEVICE = os.getenv('DEVICE', 'cpu')

from langchain_text_splitters import CharacterTextSplitter

from model.BK_rag_llm_block import BK_rag_llm_block
from model.BK_rag_retriever_block import BK_rag_retriever_block
from model.Rag_helper import Rag_helper

class Rag_chain:
  def __init__(self,llm_api_service_url = LLM_API_SERVICE_URL,  embedding_model_id = EMBEDDING_MODEL_ID, docs_path = DOCS_PATH, chuck_size = 4000, chunk_overlap = 1000):
    self.llm = BK_rag_llm_block(llm_api_service_url)
    self.retriever = BK_rag_retriever_block(embedding_model_id, docs_path, {'device': DEVICE})
    self.text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=chuck_size,
    chunk_overlap=chunk_overlap,
    length_function=len,
    is_separator_regex=True,
)
  @staticmethod
  def create_prompt(context, query):
    prompt_template = (
    "### System:\n"
    "Dưới đây là hướng dẫn mô tả một nhiệm vụ, được ghép nối với đầu vào cung cấp thêm ngữ cảnh cho câu trả lời. "
    "Viết phản hồi hoàn thành yêu cầu một cách đầy đủ nhất trích ngữ cảnh đầu vào đã cho.\n\n\n\n"
    "### Hướng dẫn:\n{instruction}\n\n"
    "### Đầu vào:\n{input}\n\n"
    "### Phản hồi:\n{output}"
    )
    input = f"Dựa vào một số ngữ cảnh được cho dưới đây, trả lời câu hỏi ở cuối.\n\n{context}\n\nCâu hỏi: {query}"
    prompt = prompt_template.format(instruction=query, input=input, output='')
    return prompt
  
  @staticmethod
  def  create_prompt_v2(context, query):
    prompt_template = (
      "===Ngữ cảnh===:\n{context_merged}\n\n"
      "===Câu hỏi===: {query}"
    )
    prompt = prompt_template.format(context_merged=context, query=query)
    print("===CHECK PROMPT===\n", len(prompt), "\n\n", prompt)
    return prompt

  def invoke(self, query):
    docs_merged = self.retriever.invoke(query)
    found_splitted_docs = self.text_splitter.split_documents(docs_merged)
    added_meta_docs = Rag_helper.add_info_docs(found_splitted_docs)
    # add_metadata_to_docs = Rag_helper.add_metadata_to_docs(added_meta_docs)
    context_combine = "\n".join([doc.page_content for doc in added_meta_docs])
    context_combine_and_cut = context_combine[:45000] # Max: 45000 characters
    prompts = [Rag_chain.create_prompt_v2(context_combine_and_cut, query)]
    outputs = [self.llm.generate(prompt) for prompt in prompts]
    return outputs
