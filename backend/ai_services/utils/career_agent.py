"""
Здесь будет агент Дани, пока просто вызов модели
"""
import json
import asyncio
from openai import AsyncOpenAI

class CareerAgent:
    def __init__(self, api_key: str):
        self.llm_client = AsyncOpenAI(api_key=api_key, base_url="https://llm.t1v.scibox.tech/v1")
        self.model_name = "Qwen2.5-72B-Instruct-AWQ"
    
    async def get_response(self, json_history):
        message_history = json.loads(json_history)

        response = await self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=message_history,
                    temperature=0.1,
                    max_tokens=4000
                )
        return response.choices[0].message.content