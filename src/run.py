# src/run.py

import subprocess
import argparse
import os

def init_db():
    subprocess.run(["python", "init_db.py"], check=True, cwd=os.path.dirname(__file__))

def send_prompt():
    subprocess.run(["python", "send_prompt.py"], check=True, cwd=os.path.dirname(__file__))

def mcp_execute():
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "mcp_execute.py")], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GeminiMCP launcher script")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database (run setup.sql)")
    parser.add_argument("--send-prompt", action="store_true", help="Run send_prompt.py")
    parser.add_argument("--mcp", action="store_true", help="Run mcp_execute.py")
    args = parser.parse_args()

    if args.init_db:
        init_db()
    elif args.send_prompt:
        send_prompt()
    elif args.mcp:
        mcp_execute()
    else:
        print("Please specify an option (--init-db / --send-prompt / --mcp)")
