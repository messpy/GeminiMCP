import os
import yaml
import sqlite3

def get_language():
    """Get the language setting from config.yaml."""
    config = get_config()
    return config.get("language", "en")

def get_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml"))
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_db_file():
    config = get_config()
    db_file = config.get("db_file")
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
