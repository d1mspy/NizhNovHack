from openai import OpenAI
from pydantic import BaseModel
import json

from .utils.prepare_profile import get_text_profile
from .utils.prompts import user_matching_prompt, system_matching_prompt


class MatchAns(BaseModel):
    score: int
    decision: str
    reasoning_report: str


class LLMAnalizer:
    def __init__(self, api_key: str):
        self.llm_client = OpenAI(api_key=api_key, base_url="https://llm.t1v.scibox.tech/v1")
        self.model_name = "Qwen2.5-72B-Instruct-AWQ"
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_match",
                    "description": "Анализирует соответствие и возвращает структурированную оценку",
                    "parameters": MatchAns.model_json_schema(),
                }
            }
        ]
    
    def match(self, user_profile, vacancy: str) -> MatchAns:
        text_profile = get_text_profile(user_profile)
        user_prompt = user_matching_prompt.format(profile=text_profile, vacancy=vacancy)

        try:
            response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_matching_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    tools=self.tools,
                    tool_choice={"type": "function", "function": {"name": "analyze_match"}},
                    temperature=0.1,
                    max_tokens=4000
                )
            if (response.choices[0].message.tool_calls and 
                len(response.choices[0].message.tool_calls) > 0):
                
                tool_call = response.choices[0].message.tool_calls[0]
                arguments = json.loads(tool_call.function.arguments)
                return MatchAns(**arguments)
            
        except Exception as e:
            print(f"Ошибка при получении ответа: {e}")

        return None
