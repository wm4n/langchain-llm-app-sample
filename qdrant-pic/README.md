## 圖片的 vector store 應用

**qdrant-pic** 此範例程式碼展示如何使用 Qdrant 和 CLIP 當作 vector store 的應用，包括：

- 建立 Qdrant collection
- 上傳圖片檔案
- 使用 similarity search

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

到 `https://qdrant.tech/` 上註冊一個帳號，用 free tier 建立一個 collection 和 API KEY

建立 `.env` 然後輸入 Qdrant cloud 上面建立的 API key 和 collection URL

```text
QDRANT_API_KEY=
QDRANT_API_URL=
COLLECTION_NAME=
```

透過 pipenv 執行上傳圖片到 Qdrant vector store

```sh
pipenv run python load_pic.py
```

應該會看到

```
共有 4 張圖片嵌入已儲存到 Qdrant！
```

使用 `query_pic.py` 搜尋相似度

```sh
pipenv run python query_pic.py query_dog.webp
```

或

```sh
pipenv run python query_pic.py query_dog2.webp
```

應該會看到

```
找到的圖片: dog.webp, 相似度得分: 0.9120784
找到的圖片: cat.webp, 相似度得分: 0.770079
找到的圖片: wolf.webp, 相似度得分: 0.6864327
找到的圖片: bird.webp, 相似度得分: 0.6563716
```
