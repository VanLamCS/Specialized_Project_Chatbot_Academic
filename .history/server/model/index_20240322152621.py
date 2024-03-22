"""# **Constants**"""

EMBEDDING_MODEL_ID= "bkai-foundation-models/vietnamese-bi-encoder"
DOCS_PATH = "drive/MyDrive/DACN/dataset/data_test"
LLM_MODEL_ID = "llm4fun/vietrag-7b-v1.0"
DEVICE = "cuda"
TORCH_DTYPE = torch.bfloat16
MAX_NEW_TOKENS = 1024

"""# **Import libraries API**

*For retriever*
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter

from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.vectorstores import FAISS

"""*For llm*"""

from transformers import GenerationConfig, TextStreamer
from transformers import LlamaForCausalLM, LlamaTokenizer, LlamaConfig
import torch
import torch.nn.functional as F

"""# **Helper**"""

class Rag_helper:
    """
    A class to provide helper functions for document processing.
    """
    @staticmethod
    def extract_info_source(doc):
        """
        Extracts information from the source field of a document's metadata.

        Args:
            doc (object): The document to extract information from.

        Returns:
            tuple: A tuple containing two elements:
                - content (str): The content part of the source information.
                - effect_year (str): The effect year part of the source information.
        """

        return doc.metadata["source"].split(".")[0].split("/")[-1].split("_")[-2:]

    @staticmethod
    def add_info_docs(docs):
        """
        Adds content and effect_year fields to the metadata of each document in a list.

        Args:
            docs (list): A list of documents.

        Returns:
            list: The list of documents with updated metadata.
        """

        for doc in docs:
            infos = Rag_helper.extract_info_source(doc)
            doc.metadata["content"] = infos[0]
            doc.metadata["effect_year"] = infos[1]
        return docs

    @staticmethod
    def add_metadata_to_docs(docs):
      for doc in docs:
        doc.page_content = "Nội dung được lấy từ tài liệu: " + doc.metadata["content"] + " và hiệu lực từ năm: " + doc.metadata["effect_year"] + "\n\n\n\n" + doc.page_content
      return docs

    @staticmethod
    def merge_docs(docs):
        """
        Merges documents with the same source, appending their page content.

        Args:
            docs (list): A list of documents.

        Returns:
            list: A list of merged documents with unique sources.
        """

        map_docs = []
        docs_merged = []

        for doc in docs:
            page_content, metadata = doc.page_content, doc.metadata

            if metadata["source"] in map_docs:
                index = map_docs.index(metadata["source"])
                docs_merged[index].page_content += "\n\n" + page_content
            else:
                docs_merged.append(doc)
                map_docs.append(metadata["source"])
        return docs_merged

    @staticmethod
    def confidence_score(scores, temperature=1.0):
        # Apply temperature scaling if needed
        if temperature != 1.0:
            scaled_scores = scores / temperature
        else:
            scaled_scores = scores

        # Apply softmax to get probabilities
        probabilities = F.softmax(scaled_scores, dim=-1)

        # Extract the maximum probability as the confidence score for each token
        confidence_scores = torch.max(probabilities, dim=-1).values

        # Calculate the average confidence score for the entire sequence
        average_confidence = confidence_scores.mean()

        return average_confidence

"""# **Retriever**"""

class BK_rag_retriever_block:
  def __init__(self, embedding_model_id, docs_path):
    self.embedding = HuggingFaceEmbeddings(model_name = embedding_model_id)
    self.char_text_splitter = CharacterTextSplitter(
       separator="\n\n",
       chunk_size=2000,
       chunk_overlap=1000,
       length_function=len,
       is_separator_regex=False,
       )
    self.docs = DirectoryLoader(docs_path).load()
    self.docs = Rag_helper.add_info_docs(self.docs)
    self.docs_chucked = self.char_text_splitter.split_documents(self.docs)

    bm25_retriever = BM25Retriever.from_documents(self.docs_chucked, search_kwargs={
        "score_threshold": 0.9,
        "k": 4
        })
    faiss_vectorstore = FAISS.from_documents(self.docs_chucked, self.embedding)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={
        "score_threshold": 0.9,
        "k": 4
        })
    self.retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5],
    search_kwargs={
        "score_threshold": 0.9,
        "k": 2
        }
    )

  def invoke(self, query):
    found_docs = self.retriever.invoke(query)
    docs_merged = Rag_helper.merge_docs(found_docs)
    return docs_merged

"""# **LMM**"""

class BK_rag_llm_block:
  def __init__(self, llm_model_id, device, torch_dtype, max_new_tokens = 1024):
    self.tokenizer = LlamaTokenizer.from_pretrained(llm_model_id)
    self.llm = LlamaForCausalLM.from_pretrained(
      llm_model_id,
      config=LlamaConfig.from_pretrained(llm_model_id),
      torch_dtype=torch_dtype
      )
    self.llm = self.llm.eval().to(device)
    self.max_new_tokens = max_new_tokens

  def generate(self, prompt):
      input_ids = self.tokenizer(prompt, return_tensors="pt")["input_ids"].to(self.llm.device)
      self.llm.eval()
      with torch.no_grad():
          generation_config = GenerationConfig(
              repetition_penalty=1.13,
              max_new_tokens=self.max_new_tokens,
              # temperature=0.2,
              # top_p=0.95,
              # top_k=20,
              # bos_token_id=tokenizer.bos_token_id,
              # eos_token_id=tokenizer.eos_token_id,
              # eos_token_id=0, # for open-end generation.
              pad_token_id=self.tokenizer.pad_token_id,
              do_sample=False,
              use_cache=True,
              return_dict_in_generate=True,
              output_attentions=False,
              output_hidden_states=False,
              output_scores=True,
              output_logits=False
          )
          streamer = TextStreamer(self.tokenizer, skip_prompt=True)
          generated = self.llm.generate(
              inputs=input_ids,
              generation_config=generation_config,
              streamer=streamer,
          )
      gen_tokens = generated["sequences"].cpu()[:, len(input_ids[0]):]
      scores = generated["logits"][0]
      sentence_confidence = Rag_helper.confidence_score(scores)
      output = self.tokenizer.batch_decode(gen_tokens)[0]
      output = output.split(self.tokenizer.eos_token)[0]

      return {"output": output.strip(), "score": sentence_confidence}
      return {"output": output.strip()}

"""# **RAG_CHAIN**: Pipeline Retrieve-LLM"""

class Rag_chain:
  def __init__(self, llm_model_id = LLM_MODEL_ID, embedding_model_id = EMBEDDING_MODEL_ID, docs_path = DOCS_PATH, device = DEVICE, torch_dtype = TORCH_DTYPE, max_new_tokens = MAX_NEW_TOKENS, chuck_size = 1000, chunk_overlap = 500):
    self.llm = BK_rag_llm_block(llm_model_id, device, torch_dtype, max_new_tokens)
    self.retriever = BK_rag_retriever_block(embedding_model_id, docs_path)
    self.text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=500,
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
    output = [self.llm.generate(prompt) for prompt in prompts[0:1]]
    return output
