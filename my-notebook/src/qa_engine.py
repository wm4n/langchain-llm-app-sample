from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence, RunnablePassthrough, RunnableLambda
from langchain.schema.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from src.document_processor import DocumentProcessor
from src.conversation_manager import ConversationManager
import os
import re

class QAEngine:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.conversation_manager = ConversationManager()
        self.llm = ChatOpenAI(temperature=0)
        self.message_history = ChatMessageHistory()
        
        # 定義提示模板
        self.qa_template = """使用提供的上下文來回答問題。請仔細閱讀上下文，並盡可能使用上下文中的信息來回答問題。

        上下文: {context}
        
        對話歷史: {chat_history}
        
        問題: {question}
        
        如果上下文中包含回答問題所需的信息，請使用該信息。
        如果上下文中沒有足夠的信息回答問題，請明確說明並嘗試使用您的基礎知識提供最佳回答。
        
        請確保您的回答準確、完整，並且直接回答問題。
        """
        
        # 創建提示對象
        self.qa_prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        # 創建問答鏈
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.document_processor.vector_store.as_retriever(
                search_kwargs={"k": 3}  # 檢索3個最相關的文件片段
            ),
            memory=None,  # 不使用內置記憶
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self.qa_prompt},
            verbose=False  # 關閉詳細輸出
        )

    def process_input(self, input_source):
        """處理輸入源（PDF 或 URL）"""
        self.document_processor.process_input(input_source)

    def _clean_text(self, text: str) -> str:
        """清理文本，移除多餘的換行和空格"""
        # 將換行符替換為空格
        text = text.replace('\n', ' ')
        # 將多個連續空格替換為單個空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def answer_question(self, question: str) -> str:
        """回答用戶問題"""
        try:
            # 獲取對話歷史並轉換為正確的格式
            conversation_history = []
            for msg in self.message_history.messages:
                if isinstance(msg, HumanMessage):
                    conversation_history.append(("Human", msg.content))
                elif isinstance(msg, AIMessage):
                    conversation_history.append(("Assistant", msg.content))
            
            # 嘗試檢索相關文件
            docs = self.document_processor.vector_store.similarity_search(question, k=3)
            
            # 印出調試信息
            debug_info = "\n\n=== 調試信息 ===\n"
            debug_info += f"檢索到的文檔數量: {len(docs)}\n\n"
            
            # 顯示 Stuff 前的文檔內容
            debug_info += "=== Stuff 前的文檔內容 ===\n"
            for i, doc in enumerate(docs):
                source = doc.metadata.get('source', 'Unknown')
                page = doc.metadata.get('page', 'Unknown')
                # 清理並格式化文檔內容
                cleaned_content = self._clean_text(doc.page_content[:200])
                debug_info += f"文檔 {i+1}:\n"
                debug_info += f"  來源: {source}\n"
                debug_info += f"  頁碼: {page}\n"
                debug_info += f"  內容片段: {cleaned_content}...\n\n"
            
            # 使用 QA 鏈處理問題
            result = self.qa_chain.invoke({
                "question": question,
                "chat_history": conversation_history
            })
            
            # 顯示 Stuff 後的完整上下文
            debug_info += "=== Stuff 後的完整上下文 ===\n"
            if "source_documents" in result:
                combined_context = "\n".join([doc.page_content for doc in result["source_documents"]])
                cleaned_context = self._clean_text(combined_context)
                debug_info += f"組合後的上下文:\n{cleaned_context}\n\n"
            
            # 構建完整的回答，先顯示參考資料
            source_info = "=== 參考資料 ===\n" + "\n".join(f"- {doc.metadata.get('source', 'Unknown')}" for doc in result.get("source_documents", []))
            answer = result["answer"]
            
            # 組合最終輸出
            final_output = f"{source_info}\n{debug_info}\n\n=== 回答 ===\n{answer}"
            
            # 保存對話
            self.conversation_manager.add_conversation(question, final_output)
            
            # 更新消息歷史
            self.message_history.add_user_message(question)
            self.message_history.add_ai_message(final_output)
            
            return final_output
            
        except Exception as e:
            error_msg = f"回答問題時出錯：{str(e)}"
            print(error_msg)
            return error_msg