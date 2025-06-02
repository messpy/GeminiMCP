# mcp_execute.py: CLI tool for receiving natural language instructions, generating Linux commands via LLM, and executing them.
# Loads DB file path from config.yaml via config.loader for unified DB access.
# Handles prompt template retrieval, LLM communication, command extraction, execution, and logging.

import os
import re
import uuid
import subprocess
from llm_client import LLMClient
from db_logger import DBLogger
from config.loader import get_db_connection

def get_llm_prompt(name="command_format"):
    """Retrieve the LLM prompt template from the database by name."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT content FROM llm_prompts WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

def extract_command(text):
    """Extract the command from the LLM response using a regex pattern."""
    match = re.search(r"\$ (.+)", text)
    if match:
        return match.group(1).strip()
    return None

def execute_command(cmd):
    """Execute the given shell command and return its output or error."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"X Command execution error: {e.stderr.strip()}"

def main():
    # Generate a session ID
    session_id = f"mcp_{uuid.uuid4().hex[:6]}"
    logger = DBLogger()
    logger.save_session(session_id)

    current_dir = os.getcwd()
    llm_client = LLMClient()

    # Retrieve the prompt template from the database
    prompt_template = get_llm_prompt(name="command_format")
    if not prompt_template:
        print("No LLM prompt template found in the database.")
        return

    print("Enter your natural language instruction (type END to submit):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    user_prompt = "\n".join(lines)

    # Compose the final prompt
    final_prompt = f"{prompt_template}\n\n{user_prompt}"

    try:
        llm_response = llm_client.send_prompt(final_prompt)
        print("\n=== LLM Response ===\n" + llm_response)
    except Exception as e:
        print(f"X LLM error: {e}")
        return

    command = extract_command(llm_response)
    if command:
        print(f"\n=== Command to Execute ===\n{command}")
        output = execute_command(command)
        print(f"\n=== Execution Result ===\n{output}")

        logger.save_log(
            session_id=session_id,
            prompt_id=None,
            command=command,
            output=output,
            tags=current_dir
        )
    else:
        print(" No command found in the LLM response.")

if __name__ == "__main__":
    main()
