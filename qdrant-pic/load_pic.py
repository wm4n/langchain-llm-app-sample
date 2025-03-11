from qdrant_client import QdrantClient
from qdrant_client.http import models
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os
import dotenv

dotenv.load_dotenv()

# 1. 載入 CLIP 模型
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# 2. 初始化 Qdrant 客戶端
client = QdrantClient(os.getenv('QDRANT_API_URL'), port=6333, api_key=os.getenv('QDRANT_API_KEY'))
collection_name = os.getenv('COLLECTION_NAME')

# 3. 重新創建集合
# 檢查集合是否存在
if client.collection_exists(collection_name="{collection_name}"):
    client.delete_collection(collection_name="{collection_name}")

# 創建新的集合
client.create_collection(
    collection_name="{collection_name}",
    vectors_config=models.VectorParams(
        size=512, # CLIP 嵌入是 512 維
        distance=models.Distance.COSINE
    )
)

# 4. 準備圖片並生成嵌入
image_paths = ["dog.webp", "cat.webp", "bird.webp", "wolf.webp"]  # 替換成你的圖片路徑
points = []
count = 0

for idx, path in enumerate(image_paths):
    # 載入圖片
    image = Image.open(path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_image_features(**inputs).numpy().tolist()[0]  # 轉為列表
    
    # 準備 Qdrant 的點（Point）
    points.append(
        models.PointStruct(
            id=idx,  # 每個圖片一個唯一 ID
            vector=embedding,
            payload={"image_path": path}  # 儲存圖片路徑作為元數據
        )
    )
    count += 1

# 5. 將嵌入上傳到 Qdrant
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"共有 {count} 張圖片嵌入已儲存到 Qdrant！")