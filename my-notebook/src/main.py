import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from src.qa_engine import QAEngine

console = Console()

def main():
    console.print(Panel.fit("歡迎使用 AI 筆記本應用", style="bold blue"))
    qa_engine = QAEngine()

    while True:
        console.print("\n請選擇操作：")
        console.print("1. 上傳 PDF 文件")
        console.print("2. 輸入 URL")
        console.print("3. 提問")
        console.print("4. 退出")
        
        choice = Prompt.ask("請輸入選項 (1-4)", choices=["1", "2", "3", "4"])

        if choice == "1":
            pdf_path = Prompt.ask("請輸入 PDF 文件路徑")
            if os.path.exists(pdf_path):
                try:
                    qa_engine.process_input(pdf_path)
                    console.print("[green]PDF 文件處理成功！[/green]")
                except Exception as e:
                    console.print(f"[red]處理 PDF 時出錯：{str(e)}[/red]")
            else:
                console.print("[red]文件不存在！[/red]")

        elif choice == "2":
            url = Prompt.ask("請輸入 URL")
            try:
                qa_engine.process_input(url)
                console.print("[green]URL 內容處理成功！[/green]")
            except Exception as e:
                console.print(f"[red]處理 URL 時出錯：{str(e)}[/red]")

        elif choice == "3":
            question = Prompt.ask("請輸入您的問題")
            try:
                answer = qa_engine.answer_question(question)
                
                # 分離參考資料和回答
                parts = answer.split("=== 回答 ===")
                if len(parts) > 1:
                    reference_and_debug = parts[0].strip()
                    answer_content = parts[1].strip()
                    
                    # 顯示參考資料和調試信息的 panel
                    console.print(Panel(reference_and_debug, title="參考資料與調試信息", border_style="yellow"))
                    
                    # 顯示回答的 panel
                    console.print(Panel(answer_content, title="回答", border_style="green"))
                else:
                    # 如果沒有找到分隔符，則顯示完整內容
                    console.print(Panel(answer, title="回答", border_style="green"))
                    
            except Exception as e:
                console.print(f"[red]回答問題時出錯：{str(e)}[/red]")

        elif choice == "4":
            console.print("[yellow]感謝使用，再見！[/yellow]")
            break

if __name__ == "__main__":
    main() 