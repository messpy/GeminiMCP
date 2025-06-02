import os
import yaml
import sqlite3

def get_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml"))
    print(f"Loading config from: {config_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_db_file():
    config = get_config()
    db_file = config.get("db_file")
    print(f"DB file from config: {db_file}")
    if not db_file:
        raise KeyError("db_file is not set in config.yaml")
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", db_file))
    if not os.path.exists(os.path.dirname(abs_path)):
        raise FileNotFoundError(f"DB directory does not exist: {os.path.dirname(abs_path)}")
    return abs_path

def get_db_connection():
    db_file = get_db_file()
    try:
        return sqlite3.connect(db_file)
    except Exception as e:
        raise ConnectionError(f"Failed to connect to DB: {db_file}\n{e}")

if __name__ == "__main__":
    # config.yamlの存在確認
    try:
        config = get_config()
        print("✅ config.yaml found and loaded.")
    except Exception as e:
        print(f"❌ {e}")

    # DBファイルのディレクトリ存在確認
    try:
        db_file = get_db_file()
        print(f"✅ DB directory exists: {os.path.dirname(db_file)}")
    except Exception as e:
        print(f"❌ {e}")
