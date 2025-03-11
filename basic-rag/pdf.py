from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores  import Chroma
from langchain_openai import OpenAI
from langchain.chat_models import init_chat_model
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
import os
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()

# 1. 讀取 PDF
loader = PyPDFLoader("../pdf/tw-wiki.pdf")
documents = loader.load()

# 2. 將文件切分區塊 (chunk)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 3. 運算 Embeddings + 4. 儲存到 Vector DB
embedding_model = OpenAIEmbeddings()
# 建立向量資料庫
vector_db = Chroma.from_documents(docs, embedding_model)

# 5. 讀取使用者輸入
user_input = "列出台灣前五大城市和他們的人口數，依照人數排序，使用繁體中文回答"  # 假設使用者輸入的問題

# 6. 用輸入搜尋相似度高的區塊
relevant_docs = vector_db.similarity_search(user_input, k=3)
for doc in relevant_docs:
    print("\n================= Document =================")
    print(doc.page_content)

# 7. 將搜尋結果與問題組成 LLM 格式
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="根據以下內容回答問題：\n{context}\n\n問題：{question}\n\n回答："
)

# 8. 輸入進 LLM
# 建立 LLM Chain
llm = OpenAI()
llm_chain = prompt_template | llm | StrOutputParser()

# 組合內容
context = "\n".join([doc.page_content for doc in relevant_docs])
response = llm_chain.invoke({"context": context, "question": user_input})

print("\n\n================= Response =================")
print(response)