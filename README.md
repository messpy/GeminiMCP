# GeminiMCP

## Overview

**GeminiMCP** is a command-line toolset for interacting with Google Gemini LLM (Large Language Model) APIs.
It allows you to send prompts, generate and execute Linux commands from natural language, and manage prompt/response logs in a local SQLite database.
The project is modular and extensible, making it easy to customize for your own workflow.

---

## Features

- Send prompts to Google Gemini LLM and receive responses
- Generate Linux commands from natural language instructions and execute them
- Log sessions, prompts, responses, and command results to a local SQLite database
- Manage prompt templates and database contents via CLI tools

---

## Initial Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourname/GeminiMCP.git
cd GeminiMCP
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requests.txt
```

### 4. Obtain a Google Gemini API Key

- Visit: https://ai.google.dev/gemini-api/docs/api-key?hl=ja
- Copy your API key.

### 5. Create a `.env` file in the project root

```env
API_KEY=your-api-key-here
```

### 6. Configure the database and model

Edit `config/config.yaml` as needed (default settings should work for most cases):

```yaml
model_name: "gemini-2.5-flash-preview-05-20"
db_file: "./data/db.db"
set_up: "setup.sql"
```

### 7. Initialize the database

```bash
python src/init_db.py
```

---

## Usage

### Send a prompt to Gemini

```bash
python src/send_prompt.py
```

### Run MCP (natural language → command execution)

```bash
python src/mcp_execute.py
```

### Manage the database (view sessions, prompts, etc.)

```bash
python src/manage_db.py --help
```

---

## Notes

- `.env` and all `.db` files are excluded from git via `.gitignore`.
- For development, always use a virtual environment (`venv`).

---
