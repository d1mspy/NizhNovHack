import json
from typing import List, Dict, Optional

from .utils.career_agent import CareerAgent
from .utils.dialog_analyzer import DialogAnalyzer, DialogAnalysis
from schemas.schemas import UserDTO
from config.config import AI_API_KEY

class AICareerService:
    def __init__(self, api_key, max_history_length: int = 10):
        """
        Инициализация сервиса чата с ИИ-агентом
        
        Args:
            api_key: ключ для работы модели
            max_history_length: максимальное количество сообщений в истории диалога
        """
        self.dialog_history: Dict[str, List[Dict]] = {}
        self.max_history_length = max_history_length
        self.career_agent = CareerAgent(api_key=api_key)
        self.dialog_analyzer = DialogAnalyzer(api_key=api_key)
    
    async def process_message(self, user_id: str, message: str) -> str:
        """
        Обработка сообщения пользователя и получение ответа от ИИ-агента
        
        Args:
            user_id: идентификатор пользователя
            message: сообщение пользователя
            
        Returns:
            Ответ ИИ-агента в виде текста
        """
        self._add_to_history(user_id, "user", message)
        history = self.get_history(user_id)

        ai_response = await self._call_ai_agent(history)

        self._add_to_history(user_id, "assistant", ai_response)
        
        return ai_response
    
    def _add_to_history(self, user_id: str, role: str, content: str):
        """
        Добавление сообщения в историю диалога
        
        Args:
            user_id: идентификатор пользователя
            role: роль отправителя (user/assistant)
            content: содержание сообщения
        """
        if user_id not in self.dialog_history:
            self.dialog_history[user_id] = []
        
        self.dialog_history[user_id].append({
            "role": role,
            "content": content
        })
        
        if len(self.dialog_history[user_id]) > self.max_history_length:
            self.dialog_history[user_id] = self.dialog_history[user_id][-self.max_history_length:]
    
    async def analyze_dialog(self, user_id: str, user_profile: Dict) -> Dict:
        history = self.get_history(user_id)
        
        analysis = await self.dialog_analyzer.analyze(
            history, 
            user_profile['hard_skills'], 
            user_profile['experience_description'],
            user_profile['career_expectations']
        )
        
        if analysis:
            return self._update_profile(user_profile, analysis)
        
        return user_profile
    
    def _update_profile(self, profile: Dict, analysis: DialogAnalysis) -> Dict:
        """
        Обновление профиля пользователя на основе анализа диалога
        """
        for skill in analysis.new_hard_skills:
            if skill not in profile['hard_skills']:
                profile['hard_skills'].append(skill)

        if analysis.new_experience:
            if profile['experience_description']:
                profile['experience_description'] += " " + analysis.new_experience
            else:
                profile['experience_description'] = analysis.new_experience
        
        if analysis.career_expectations:
            profile['career_expectations'] = analysis.career_expectations
        
        return profile
    
    def _get_history_json(self, user_id: str) -> str:

        history = self.dialog_history.get(user_id, [])
        return json.dumps(history, ensure_ascii=False, indent=2)
    
    async def _call_ai_agent(self, history: str) -> str:

        return await self.career_agent.get_response(history)
    
    def get_history(self, user_id: str) -> List[Dict]:

        return self.dialog_history.get(user_id, [])
    
    def clear_history(self, user_id: str):

        if user_id in self.dialog_history:
            del self.dialog_history[user_id] 

ai_service = AICareerService(api_key = AI_API_KEY)