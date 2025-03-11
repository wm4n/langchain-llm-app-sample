import argparse
from qdrant_client import QdrantClient
from qdrant_client.http import models
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os
import dotenv

# 設定命令列參數
parser = argparse.ArgumentParser(description='搜尋相似圖片')
parser.add_argument('image_path', type=str, help='要搜尋的圖片檔案路徑')
args = parser.parse_args()

# 檢查圖片檔名是否有提供
if(args.image_path is None):
    raise ValueError("請提供要搜尋的圖片檔案路徑")

# 檢查圖片檔案是否存在
if(not os.path.exists(args.image_path)):
    raise FileNotFoundError(f"找不到圖片檔案: {args.image_path}")

dotenv.load_dotenv()

# 1. 載入 CLIP 模型
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 2. 初始化 Qdrant 客戶端
client = QdrantClient(os.getenv('QDRANT_API_URL'), port=6333, api_key=os.getenv('QDRANT_API_KEY'))
collection_name = os.getenv('COLLECTION_NAME')

# 3. 載入查詢圖片並生成嵌入
query_image_path = args.image_path  # 從命令列參數取得圖片路徑
query_image = Image.open(query_image_path).convert("RGB")
query_inputs = processor(images=query_image, return_tensors="pt")
with torch.no_grad():
    query_embedding = model.get_image_features(**query_inputs).numpy().tolist()[0]

# 4. 在 Qdrant 中搜尋相似圖片
search_result = client.query_points(
    collection_name=collection_name,
    query=query_embedding,  # 查詢向量
    limit=4,
    with_payload=True
)

# 5. 顯示結果
for result in search_result.points:
    image_path = result.payload["image_path"]
    score = result.score  # 餘弦相似度得分（越高越相似）
    print(f"找到的圖片: {image_path}, 相似度得分: {score}")