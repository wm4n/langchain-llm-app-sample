## LCEL 用法

**chain-demo** 此範例程式碼展示如何使用 LangChain LCEL，包括：

- llm invoke 和純文字輸入
- llm 和純文字輸入，使用 LCEL 語法
- llm 和輸入 preprocess

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
pipenv run python chain.py
```
