## 基礎 RAG 應用

**basic-rag** 此範例程式碼展示如何使用 LangChain 開發一個基本的 LLM RAG 應用程式，包括：

- 讀取 PDF 文件
- 切分文本為區塊
- 計算文本的嵌入向量並存入向量資料庫
- 接收使用者輸入並檢索相似內容
- 使用大型語言模型生成回應

## 安裝

請按照以下步驟進行安裝：

安裝 pipenv 來管理 python 環境

```sh
brew install pipenv
```

建立專案目錄，進入該入目錄

```sh
pipenv --python 3.12
```

建立專案目錄，進入該入目錄

```sh
pipenv install
```

建立 `.env`然後輸入 OpenAI API KEY

```text
OPENAI_API_KEY=[YOUR OPENAI token]
```

透過 pipenv 執行

```sh
pipenv run python pdf.py
```
