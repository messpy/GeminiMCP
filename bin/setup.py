# setup.py: Project setup script for GeminiMCP
# - Creates the SQLite DB using setup.sql
# - Creates .env file and inserts API key from user input
# - Calls check.py for post-setup validation

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from config.loader import get_db_connection

SETUP_SQL = os.path.join(os.path.dirname(__file__), "..", "config", "setup.sql")
ENV_FILE = os.path.join(os.path.dirname(__file__), "..", ".env")
CHECK_SCRIPT = os.path.join(os.path.dirname(__file__), "check.py")

def create_db():
    """Initialize the database using setup.sql."""
    if not os.path.exists(SETUP_SQL):
        print(f"X setup.sql not found at {SETUP_SQL}")
        return False
    conn = get_db_connection()
    try:
        with open(SETUP_SQL, "r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        print("OK! DB has been initialized using setup.sql!")
        return True
    except Exception as e:
        print(f"X DB initialization error: {e}")
        return False
    finally:
        conn.close()

def create_env():
    """Create .env file and insert API key from user input."""
    if os.path.exists(ENV_FILE):
        print(f".env already exists at {ENV_FILE}")
        return
    api_key = input("Enter your Gemini API key: ").strip()
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(f'API_KEY="{api_key}"\n')
    print(f".env file created at {ENV_FILE}")

def check_files():
    """Call check.py for post-setup validation."""
    if not os.path.exists(CHECK_SCRIPT):
        print(f"X check.py not found at {CHECK_SCRIPT}")
        return
    print("Running check.py for validation...")
    os.system(f'python "{CHECK_SCRIPT}"')

def main():
    print("=== GeminiMCP Project Setup ===")
    create_db()
    create_env()
    check_files()
    print("Setup completed.")

if __name__ == "__main__":
    main()
