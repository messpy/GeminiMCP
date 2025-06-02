# DBLogger: Handles saving sessions, prompts, LLM answers, and logs to the SQLite database.
# Uses config.loader.get_db_connection() for unified DB access.
# All DB operations (insertions) are wrapped in methods for each entity.

from datetime import datetime
from config.loader import get_db_connection

class DBLogger:
    def save_session(self, session_id):
        now = datetime.now().isoformat()
        self._execute(
            "INSERT OR IGNORE INTO sessions (session_id, created_at) VALUES (?, ?)",
            (session_id, now)
        )

    def save_prompt(self, session_id, prompt_text):
        now = datetime.now().isoformat()
        self._execute(
            "INSERT INTO prompts (session_id, prompt_text, created_at) VALUES (?, ?, ?)",
            (session_id, prompt_text, now)
        )

    def save_llm_answer(self, prompt_id, response_text, summary=None, tags=None):
        now = datetime.now().isoformat()
        self._execute(
            "INSERT INTO llm_answers (prompt_id, response_text, summary, tags, created_at) VALUES (?, ?, ?, ?, ?)",
            (prompt_id, response_text, summary, tags, now)
        )

    def save_log(self, session_id, prompt_id, command, output, notes=None, tags=None):
        now = datetime.now().isoformat()
        self._execute(
            "INSERT INTO logs (session_id, prompt_id, command, output, notes, tags, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (session_id, prompt_id, command, output, notes, tags, now)
        )

    def _execute(self, sql, params):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(f"❌ DB save error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
