# src/llm_client.py

# LLMClient: Handles communication with the LLM API (Google Generative Language).
# Loads API key and model name from .env or config.yaml via config.loader.
# Provides a method to send prompts and receive responses from the LLM.

import requests
import json
import os
from dotenv import load_dotenv
from config.loader import get_config

class LLMClient:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
        config = get_config()
        # Get API key from environment variable, fallback to config.yaml if not set
        self.api_key = os.getenv("API_KEY") or config.get("api_key")
        self.model_name = config.get("model_name")
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

    def send_prompt(self, prompt):
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }
        response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
