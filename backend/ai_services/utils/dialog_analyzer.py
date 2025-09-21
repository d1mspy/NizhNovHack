from openai import AsyncOpenAI
from pydantic import BaseModel
import json
from typing import Dict, List, Optional

from config.config import AI_API_KEY
from .prompts import system_dialog_analyze_prompt


class DialogAnalysis(BaseModel):
    new_hard_skills: List[str] = []
    new_experience: str = ""
    career_expectations: str = ""

class DialogAnalyzer:
    def __init__(self, api_key: str):
        self.llm_client = AsyncOpenAI(api_key=api_key, base_url="https://llm.t1v.scibox.tech/v1")
        self.model_name = "Qwen2.5-72B-Instruct-AWQ"
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_dialog",
                    "description": "Анализирует диалог и извлекает новую информацию о пользователе",
                    "parameters": DialogAnalysis.model_json_schema(),
                }
            }
        ]
        

    async def analyze(self, 
                      dialog_history: List[Dict], 
                      current_skills: List[str], 
                      current_experience: str,
                      career_expectations: str) -> Optional[DialogAnalysis]:
        formatted_history = self._format_history(dialog_history)
        system_prompt = system_dialog_analyze_prompt.format(
            current_skills=", ".join(current_skills),
            current_experience=current_experience,
            career_expectations=career_expectations
        )

        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": formatted_history},
                ],
                tools=self.tools,
                tool_choice={"type": "function", "function": {"name": "analyze_dialog"}},
                temperature=0,
            )
            
            if (response.choices[0].message.tool_calls and 
                len(response.choices[0].message.tool_calls) > 0):
                
                tool_call = response.choices[0].message.tool_calls[0]
                arguments = json.loads(tool_call.function.arguments)
                return DialogAnalysis(**arguments)
            
        except Exception as e:
            print(f"Ошибка при анализе диалога: {e}")

        return None

    def _format_history(self, history: List[Dict]) -> str:
        return "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in history
        ])
