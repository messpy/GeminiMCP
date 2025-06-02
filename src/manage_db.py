# manage_db.py: CLI tool for viewing and managing database contents.
# Supports listing sessions, prompts, LLM answers, and managing LLM prompt templates.
# Loads DB file path from config.yaml via config.loader for unified DB access.

import os
from datetime import datetime
import argparse
from config.loader import get_db_connection

def view_sessions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT session_id, created_at FROM sessions ORDER BY created_at DESC")
    rows = cur.fetchall()
    print("\n=== セッション一覧 ===")
    print(f"{'Session ID':<15} | {'Created At'}")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<15} | {row[1]}")
    conn.close()

def view_prompts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT prompt_id, session_id, prompt_text, created_at FROM prompts ORDER BY created_at DESC")
    rows = cur.fetchall()
    print("\n=== プロンプト一覧 ===")
    for row in rows:
        print(f"[{row[0]}] ({row[1]}) {row[2]} @ {row[3]}")
    conn.close()

def view_llm_answers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT answer_id, prompt_id, response_text, created_at FROM llm_answers ORDER BY created_at DESC")
    rows = cur.fetchall()
    print("\n=== LLM応答一覧 ===")
    for row in rows:
        print(f"[{row[0]}] (Prompt {row[1]}) {row[2]} @ {row[3]}")
    conn.close()

def select_llm_prompt():
    """Interactively select and display an LLM prompt by name."""
    name = input("Prompt name: ").strip()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM llm_prompts WHERE name = ?", (name,))
        rows = cur.fetchall()
        if rows:
            print("LLM Prompt Details:")
            for row in rows:
                print(f"Name: {row[1]}, \nDescription: {row[2]},\nContent: {row[3]}, \nCreated At: {row[4]}")
        else:
            print(f"LLM prompt '{name}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def insert_llm_prompt():
    """Interactively insert a new LLM prompt (multi-line content supported)."""
    name = input("Prompt name: ").strip()
    description = input("Description: ").strip()
    print("Enter content. Finish with a single line containing END:")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    content = "\n".join(lines)
    conn = get_db_connection()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    try:
        cur.execute("SELECT * FROM llm_prompts WHERE name = ?", (name,))
        if cur.fetchone():
            print(f"LLM prompt '{name}' already exists. Please use update.")
            return
        cur.execute(
            "INSERT INTO llm_prompts (name, description, content, created_at) VALUES (?, ?, ?, ?)",
            (name, description, content, now)
        )
        conn.commit()
        print(f"New LLM prompt '{name}' has been added.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_llm_prompt():
    """Interactively update an existing LLM prompt or insert if not exists (multi-line content supported)."""
    name = input("Prompt name: ").strip()
    description = input("Description: ").strip()
    print("Enter content. Finish with a single line containing END:")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    content = "\n".join(lines)
    conn = get_db_connection()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    try:
        cur.execute("""
            INSERT INTO llm_prompts (name, description, content, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                description=excluded.description,
                content=excluded.content,
                created_at=excluded.created_at
        """, (name, description, content, now))
        conn.commit()
        print(f"LLM prompt '{name}' has been updated!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description="DB管理ツール")
    parser.add_argument("--sessions", action="store_true", help="セッション一覧表示")
    parser.add_argument("--prompts", action="store_true", help="プロンプト一覧表示")
    parser.add_argument("--llm", action="store_true", help="LLM応答一覧表示")
    parser.add_argument("--prompt-template", choices=["select", "insert", "update"], help="プロンプトテンプレート管理")
    args = parser.parse_args()

    if args.sessions:
        view_sessions()
    elif args.prompts:
        view_prompts()
    elif args.llm:
        view_llm_answers()
    elif args.prompt_template:
        if args.prompt_template == "select":
            select_llm_prompt()
        elif args.prompt_template == "insert":
            insert_llm_prompt()
        elif args.prompt_template == "update":
            update_llm_prompt()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
