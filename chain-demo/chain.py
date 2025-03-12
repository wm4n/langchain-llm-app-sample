from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableLambda
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()

# 1. llm 和純文字輸入
print("=====================================")
print("1. llm 和純文字輸入\n")
      
llm = ChatOpenAI(model="gpt-3.5-turbo")
result = llm.invoke("告訴我一個笑話")
print(result.content)

# 2. llm 和純文字輸入，使用 LCEL 語法
print("\n=====================================")
print("2. llm 和純文字輸入，使用 LCEL 語法\n")
      
prompt = RunnableLambda(lambda topic : f"告訴我一個關於{topic}的笑話 ")
llm = ChatOpenAI(model="gpt-3.5-turbo")
chain = prompt | llm
result = chain.invoke("找工作")
print(result.content)

# 3. llm 和輸入 filter
print("\n=====================================")
print("3. llm 和輸入 preprocess\n")

# 如果包含 "笑話" 這個關鍵字，就 exception
preprocess = RunnableLambda(lambda text: text if "笑話" not in text else (_ for _ in ()).throw(Exception("不準提「笑話」！")))
llm = ChatOpenAI(model="gpt-3.5-turbo")
try:
    result = (preprocess | llm).invoke("告訴我一個笑話")
    print(result.content)
except Exception as e:
    print(e)