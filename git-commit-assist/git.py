from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import argparse
import os

# 讀取 .env 檔案
load_dotenv()

# 設定命令列參數
parser = argparse.ArgumentParser(description='根據 git diff 生成 commit message')
parser.add_argument('diff_file', type=str, help='要讀取的 git diff 檔案名稱')
args = parser.parse_args()

# 確保檔案存在
if not os.path.exists(args.diff_file):
    print(f"錯誤：找不到檔案 {args.diff_file}")
    exit(1)

# 讀取 git diff 檔案內容
with open(args.diff_file, "r", encoding="utf-8") as file:
    diff_content = file.read()

# 建立 PromptTemplate
template = """
以下是 git diff 檔案的內容：
{diff}

請根據 git diff，用繁體中文、台灣用語生成一個 commit message，並包含：
1. commit message 的主旨（簡短描述）
2. commit message 的類型（feat, fix, docs, style, refactor, perf, test, chore）
3. commit changes 的內容

範例輸出：
```
feat: 新增使用者登入功能
- 新增登入頁面
- 新增登入 API
- 新增登入測試
```

輸出只要 commit message，不要其他內容。
"""
prompt = PromptTemplate(input_variables=["diff"], template=template)

# 建立 LLM
llm = ChatOpenAI(model="gpt-4.1", 
                 temperature=0.1)

# 設定輸出解析器
output_parser = StrOutputParser()

# 建立 Chain
chain = prompt | llm | output_parser

# 執行 Chain，生成 commit message
response = chain.invoke({"diff": diff_content})

# 印出結果
print(response)
