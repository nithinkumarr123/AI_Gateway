import asyncio
import httpx
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    def __init__(self):
        self.fast_model_config = {
            'name': 'Groq - Llama 3.1 8B',
            'api_key': os.getenv('GROQ_API_KEY'),
            'model': 'llama-3.1-8b-instant',
            'endpoint': 'https://api.groq.com/openai/v1/chat/completions'
        }
        
        self.capable_model_config = {
            'name': 'Google Gemini Pro',
            'api_key': os.getenv('GEMINI_API_KEY'),
            'model': 'gemini-pro',
            'endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
        }
        
        self.request_count = 0
    
    async def get_response(self, prompt: str, model_type: str) -> str:
        try:
            self.request_count += 1
            
            if model_type == 'fast':
                return await self._call_groq(prompt)
            else:
                return await self._call_gemini(prompt)
                
        except Exception as e:
            return f"[Error] {str(e)}"
    
    async def _call_groq(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.fast_model_config['endpoint'],
                headers={
                    'Authorization': f"Bearer {self.fast_model_config['api_key']}",
                    'Content-Type': 'application/json'
                },
                json={
                    'model': self.fast_model_config['model'],
                    'messages': [
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 500
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"[Groq Error] Status: {response.status_code}"
    
    async def _call_gemini(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.capable_model_config['endpoint'],
                params={'key': self.capable_model_config['api_key']},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    return data['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "[Gemini Error] No response"
            else:
                return f"[Gemini Error] Status: {response.status_code}"