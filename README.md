# GeminiMCP

## Initial Setup

```bash
git clone https://github.com/yourname/GeminiMCP.git
cd GeminiMCP
pip install -r requirements.txt
```


Obtain a Google Gemini API Key

https://ai.google.dev/gemini-api/docs/api-key?hl=ja

Create a .env file and add your API key:
```.env
GEMINI_API_KEY=your-api-key-here
```

Initialize the database (if required)
```bash
python src/init_db.py

```

Send a prompt to Gemini
```bash
python src/send_prompt.py "Hello World"
```

Run MCP
```bash
python src/mcp_execute.py
```
