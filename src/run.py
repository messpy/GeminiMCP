# src/run.py

import subprocess
import argparse
import os

def init_db():
    subprocess.run(["python", "init_db.py"], check=True, cwd=os.path.dirname(__file__))

def send_prompt():
    subprocess.run(["python", "send_prompt.py"], check=True, cwd=os.path.dirname(__file__))

def mcp_execute():
    subprocess.run(["python", "mcp_execute.py"], check=True, cwd=os.path.dirname(__file__))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PiLLMプロジェクト起動スクリプト")
    parser.add_argument("--init-db", action="store_true", help="DB初期化（setup.sql実行）")
    parser.add_argument("--send-prompt", action="store_true", help="send_prompt.py 実行")
    parser.add_argument("--mcp", action="store_true", help="mcp_execute.py 実行")
    args = parser.parse_args()

    if args.init_db:
        init_db()
    elif args.send_prompt:
        send_prompt()
    elif args.mcp:
        mcp_execute()
    else:
        print("オプションを指定してください (--init-db / --send-prompt / --mcp)")
