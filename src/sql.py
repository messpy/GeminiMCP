# src/sql.py

import sqlite3
from config.loader import get_db_file

DB_FILE = get_db_file()

def execute_sql(sql, params=None, fetch=False):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        if fetch:
            return cur.fetchall()
        else:
            conn.commit()
            return True
    except Exception as e:
        print(f"X SQL execution error: {e}")
        return None
    finally:
        conn.close()

def get_sql_by_name(sql_name):
    result = execute_sql("SELECT sql_text FROM sql_queries WHERE sql_name = ?", (sql_name,), fetch=True)
    return result[0][0] if result else None

def run_sql_by_name(sql_name, params=None):
    sql_text = get_sql_by_name(sql_name)
    if not sql_text:
        print(f"X SQL '{sql_name}' not found")
        return None
    return execute_sql(sql_text, params, fetch=True if sql_text.lower().startswith("select") else False)
