-- PiLLMプロジェクト: データベース初期化SQL

DROP TABLE IF EXISTS sql_queries;
DROP TABLE IF EXISTS prompts;
DROP TABLE IF EXISTS llm_answers;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS llm_prompts;

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    created_at TEXT
);

CREATE TABLE prompts (
    prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    prompt_text TEXT,
    created_at TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

CREATE TABLE llm_answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER,
    response_text TEXT,
    summary TEXT,
    tags TEXT,
    created_at TEXT,
    FOREIGN KEY(prompt_id) REFERENCES prompts(prompt_id)
);

CREATE TABLE logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    prompt_id INTEGER,
    command TEXT,
    output TEXT,
    notes TEXT,
    tags TEXT,
    created_at TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id),
    FOREIGN KEY(prompt_id) REFERENCES prompts(prompt_id)
);

CREATE TABLE sql_queries (
    sql_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sql_name TEXT,
    sql_text TEXT,
    category TEXT,
    created_at TEXT
);

CREATE TABLE llm_prompts (
    prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE, -- ←ここを追加
    description TEXT,
    content TEXT,
    created_at TEXT
);

INSERT INTO llm_prompts (name, description, content, created_at) VALUES (
    'command_format',
    'Generate a Linux command from a natural language instruction.',
    'Please convert the following instruction into a Linux shell command. Output only the command, prefixed by a dollar sign ($).',
    datetime('now')
);
