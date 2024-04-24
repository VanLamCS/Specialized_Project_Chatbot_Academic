"""*For retriever*"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter

from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

from model.Rag_helper import Rag_helper

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
        "k": 8
        })
    # db = Chroma.from_documents(self.docs_chucked, self.embeddings)
    # embedding_retriever = db.as_retriever(search_kwargs={
    #     "score_threshold": 0.9,
    #     "k": 4
    #     })
    faiss_vectorstore = FAISS.from_documents(self.docs_chucked, self.embedding)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={
        "score_threshold": 0.9,
        "k": 8
        })
    self.retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5],
    search_kwargs={
        "score_threshold": 0.9,
        "k": 8
        }
    )

  def invoke(self, query):
    found_docs = self.retriever.invoke(query)
    docs_merged = Rag_helper.merge_docs(found_docs)
    return docs_merged