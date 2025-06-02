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
    prompts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "prompts"))
    prompt_file = os.path.join(prompts_dir, f"{name}.prompty")
    if not os.path.exists(prompt_file):
        print(f"X Prompt file not found: {prompt_file}")
        return ""
    with open(prompt_file, encoding="utf-8") as f:
        return f.read()

def extract_command_and_comment(text):
    """
    Extract the command and comment from the LLM response.
    Returns (command, comment) tuple.
    """
    match = re.search(r"\$ (.+)", text)
    if not match:
        return None, None
    line = match.group(1).strip()
    if "#" in line:
        cmd, comment = line.split("#", 1)
        return cmd.strip(), comment.strip()
    else:
        return line, None

def execute_command(cmd):
    """Execute the given shell command and return its output or error."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"X Command execution error: {e.stderr.strip()}"

def extract_paths_from_command(command):
    """Extract likely file/directory paths from a shell command."""
    # 例: mkdir test && touch test/a.txt → ['test', 'test/a.txt']
    paths = []
    for part in command.split("&&"):
        tokens = part.strip().split()
        if tokens and tokens[0] in ["touch", "mkdir", "cp", "mv"]:
            # touch/mkdirは複数ファイル対応
            paths += [os.path.abspath(arg) for arg in tokens[1:]]
    return paths

def main():
    # Generate a session ID
    session_id = f"mcp_{uuid.uuid4().hex[:6]}"
    logger = DBLogger()
    logger.save_session(session_id)

    current_dir = os.getcwd()
    llm_client = LLMClient()

    # Retrieve the prompt template from the database
    prompt_template = get_llm_prompt(name="mcp")
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
    except Exception as e:
        print(f"X LLM error: {e}")
        return

    command, comment = extract_command_and_comment(llm_response)
    if command:
        # Show current working directory (pwd)
        pwd = os.getcwd()
        print("== Response from LLM ==")
        print(f"{pwd}$ {command}\n")

        # Execute the command and print output
        output = execute_command(command)
        if output:
            print(output)

        # Print the LLM's comment (after #)
        if comment:
            print(f"LLM comment: {comment}")

        # DB保存
        logger.save_mcp_log(
            session_id=session_id,
            is_error=1 if output and output.startswith("X Command execution error") else 0,
            status_code=None,
            error_message=output if output and output.startswith("X Command execution error") else None,
            prompt_text=user_prompt,
            command=command,
            command_type="shell",
            result=output,
            llm_response=llm_response,
            tags=current_dir,
            duration=None,
            user=None
        )
        print(f"Session ID: {session_id}")
    else:
        print("No command found in the LLM response.")
        print("=== LLM Raw Response ===")
        print(llm_response)

if __name__ == "__main__":
    main()
