import sqlite3
import os
from datetime import datetime
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

class ConversationManager:
    def __init__(self):
        self.db_path = os.getenv("CONVERSATION_DB_PATH")
        self._init_db()

    def _init_db(self):
        """初始化數據庫表"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    question TEXT,
                    answer TEXT
                )
            """)

    def add_conversation(self, question: str, answer: str):
        """添加新的對話"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO conversations (timestamp, question, answer) VALUES (?, ?, ?)",
                (datetime.now(), question, answer)
            )

    def get_recent_conversations(self, limit: int = 5) -> List[Tuple[str, str]]:
        """獲取最近的對話"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT question, answer FROM conversations ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            return cursor.fetchall()

    def get_conversation_history(self) -> str:
        """獲取格式化的對話歷史"""
        conversations = self.get_recent_conversations()
        history = ""
        for question, answer in reversed(conversations):
            history += f"問題: {question}\n回答: {answer}\n\n"
        return history 