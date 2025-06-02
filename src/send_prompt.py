# src/send_prompt.py

from llm_client import LLMClient
from db_logger import DBLogger
import uuid

def main():
    logger = DBLogger()
    session_id = f"llm_{uuid.uuid4().hex[:6]}"
    logger.save_session(session_id)

    print("Enter your prompt (type END to submit):")
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
        print("\n=== Response ===")
        print(reply)
        logger.save_llm_answer(prompt_id=None, response_text=reply)  # prompt_id can be linked later
        print(f"DB save completed: session_id={session_id}")
    except Exception as e:
        print("API error:", e)

if __name__ == "__main__":
    main()
