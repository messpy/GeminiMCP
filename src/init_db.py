# This script initializes the SQLite database using setup.sql.
# It loads the DB file path from config.yaml via config.loader.

import os
from config.loader import get_db_connection

SETUP_SQL = os.path.join(os.path.dirname(__file__), "..", "config", "setup.sql")

def init_db():
    """Initialize the database using setup.sql."""
    if not os.path.exists(SETUP_SQL):
        print(f"X setup.sql not found at {SETUP_SQL}")
        return
    conn = get_db_connection()
    try:
        with open(SETUP_SQL, "r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        print(f"OK! DB has been initialized using setup.sql!")
    except Exception as e:
        print(f"X DB initialization error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
