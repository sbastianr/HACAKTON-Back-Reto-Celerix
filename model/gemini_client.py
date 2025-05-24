import os

import requests
import json
from dotenv import load_dotenv


class GeminiClient:
    def __init__(self, model="gemini-2.0-flash"):
        load_dotenv(dotenv_path="../.env")
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate_content(self, prompt):
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")