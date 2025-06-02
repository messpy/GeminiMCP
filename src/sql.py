# src/sql.py

import sqlite3
import os
from datetime import datetime

import yaml

# 設定ファイルからDBパスを取得
with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

DB_FILE = os.path.join(os.path.dirname(__file__), config.get("db_file", "pillmdb.db"))

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
        print(f"❌ SQL実行エラー: {e}")
        return None
    finally:
        conn.close()

def get_sql_by_name(sql_name):
    result = execute_sql("SELECT sql_text FROM sql_queries WHERE sql_name = ?", (sql_name,), fetch=True)
    return result[0][0] if result else None

def run_sql_by_name(sql_name, params=None):
    sql_text = get_sql_by_name(sql_name)
    if not sql_text:
        print(f"⚠️ SQL '{sql_name}' が見つかりません")
        return None
    return execute_sql(sql_text, params, fetch=True if sql_text.lower().startswith("select") else False)
