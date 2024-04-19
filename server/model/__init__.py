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
  def __init__(self,llm_api_service_url = LLM_API_SERVICE_URL,  embedding_model_id = EMBEDDING_MODEL_ID, docs_path = DOCS_PATH, chuck_size = 2000, chunk_overlap = 1000):
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
    "Below is an instruction that describes a task, paired with an input that provides further context. "
    "Write a response that appropriately completes the request.\n\n\n\n"
    "### Instruction:\n{instruction}\n\n"
    "### Input:\n{input}\n\n"
    "### Response:\n{output}"
    )
    input = f"Dựa vào một số ngữ cảnh được cho dưới đây, trả lời câu hỏi ở cuối.\n\n{context}\n\nQuestion: {query}"
    prompt = prompt_template.format(instruction=query, input=input, output='')
    return prompt

  def invoke(self, query):
    docs_merged = self.retriever.invoke(query)
    found_splitted_docs = self.text_splitter.split_documents(docs_merged)
    added_meta_docs = Rag_helper.add_info_docs(found_splitted_docs)

    prompts = [Rag_chain.create_prompt(doc.page_content, query) for doc in added_meta_docs]
    outputs = [self.llm.generate(prompt) for prompt in prompts]
    return outputs
