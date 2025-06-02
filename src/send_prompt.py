# src/send_prompt.py

from llm_client import LLMClient
from db_logger import DBLogger
import uuid

def main():
    logger = DBLogger()
    session_id = f"llm_{uuid.uuid4().hex[:6]}"
    logger.save_session(session_id)

    print("プロンプトを入力してください（ENDで送信）：")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    prompt = "\n".join(lines)

    logger.save_prompt(session_id, prompt)

    try:
        llm = LLMClient()
        reply = llm.send_prompt(prompt)
        print("\n=== 応答 ===")
        print(reply)
        logger.save_llm_answer(prompt_id=None, response_text=reply)  # prompt_idは後で結合可
        print(f"DB保存完了: セッションID={session_id}")
    except Exception as e:
        print("APIエラー:", e)

if __name__ == "__main__":
    main()
