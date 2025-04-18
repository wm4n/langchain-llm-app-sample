import os
from typing import List, Union
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = Chroma(
            collection_name="document_collection",
            persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY"),
            embedding_function=self.embeddings
        )

    def process_pdf(self, pdf_path: str) -> None:
        """處理 PDF 文件並將其添加到向量存儲中"""
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        texts = self.text_splitter.split_documents(pages)
        self.vector_store.add_documents(texts)

    def process_url(self, url: str) -> None:
        """處理 URL 並將其內容添加到向量存儲中"""
        loader = WebBaseLoader(url)
        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)
        self.vector_store.add_documents(texts)

    def process_input(self, input_source: Union[str, List[str]]) -> None:
        """處理輸入源（PDF 文件路徑或 URL）"""
        if isinstance(input_source, str):
            input_source = [input_source]
        
        for source in input_source:
            if source.lower().endswith('.pdf'):
                self.process_pdf(source)
            elif source.startswith(('http://', 'https://')):
                self.process_url(source)
            else:
                raise ValueError(f"不支持的輸入源: {source}") 