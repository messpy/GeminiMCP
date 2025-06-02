# src/update_llm_prompt.py

import sqlite3
import os
from datetime import datetime
import subprocess
from config.loader import get_config, get_db_file, get_language

config = get_config()
DB_FILE = get_db_file()
lang = get_language()


def select_llm_prompt(name):
    """Select and display an LLM prompt by name."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM llm_prompts WHERE name = ?", (name,))
        rows = cur.fetchall()
        if rows:
            print("LLM Prompt Details:")
            for row in rows:
                print(f"Name: {row[0]}, \nDescription: {row[1]},\nContent: {row[2]}, \nCreated At: {row[3]}")
        else:
            print(f"LLM prompt '{name}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def insert_llm_prompt(name, description, content):
    """Insert a new LLM prompt if it does not exist."""
    conn = sqlite3.connect(DB_FILE)
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

def update_llm_prompt(name, description, content):
    """Update an existing LLM prompt or insert if not exists (upsert)."""
    conn = sqlite3.connect(DB_FILE)
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

if __name__ == "__main__":
    name = "command_format"
    description = "For Linux command format output"
    pwd_cmd = subprocess.run("pwd", capture_output=True,text=True ).stdout
    tree_cmd = subprocess.run(
        "tree -I '__pycache__|venv|.venv|.mypy_cache|.pytest_cache|*.pyc|*.pyo|*.egg-info|.git|.idea'",
        capture_output=True, text=True, shell=True
    ).stdout

    content = f"""
        You are a Linux administrator and adviser.
        Please interpret the user's prompt and execute the command in one line.
        Always put the command after $.
        If there are multiple lines, connect them with &&.
        AND Comment the command with #.
        and output the result in the following format:
        ALL Comment output language is {lang}

        Current dir is {pwd_cmd}$
        tree -I '__pycache__|venv|.venv|.mypy_cache|.pytest_cache|*.pyc|*.pyo|*.egg-info|.git|.idea'$

        {tree_cmd}

        """

    select = input("LLM prompt management\n1.SELECT\n2.INSERT\n3.UPDATE: ")
    if select == '1':
        select_llm_prompt(name)
    elif select == '2':
        insert_llm_prompt(name, description, content)
    elif select == '3':
        update_llm_prompt(name, description, content)
    else:
        print("Invalid selection. Please enter 1, 2, or 3.")
