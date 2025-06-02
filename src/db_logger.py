# DBLogger: Handles saving sessions, prompts, LLM answers, and logs to the SQLite database.
# Uses config.loader.get_db_connection() for unified DB access.
# All DB operations (insertions) are wrapped in methods for each entity.

from datetime import datetime
from config.loader import get_db_connection

def _safe_str(val):
    if isinstance(val, str):
        return val.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    return val

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

    def save_mcp_log(self, session_id, is_error, status_code, error_message, prompt_text, command, command_type, result, llm_response, tags, duration, user):
        now = datetime.now().isoformat()
        self._execute(
            """INSERT INTO mcp_logs (
                session_id, is_error, status_code, error_message, prompt_text, command, command_type, result, llm_response, tags, duration, user, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (session_id, is_error, status_code, error_message, prompt_text, command, command_type, result, llm_response, tags, duration, user, now)
        )

    def _execute(self, sql, params):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            safe_params = tuple(_safe_str(p) for p in params)
            cur.execute(sql, safe_params)
            conn.commit()
        except Exception as e:
            print(f"X DB save error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
