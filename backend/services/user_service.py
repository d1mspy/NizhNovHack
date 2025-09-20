from uuid import UUID
from typing import Tuple

from repositories.db.user_repository import user_repository
from schemas.schemas import UserDTO, UserLogin
from ai_services.career import ai_service
from typing import List
from utils.concatination import user_to_single_line
from schemas.schemas import Skills

class UserService:
    def __init__(self):
        self.repository = user_repository
        
    async def put_user(self, user: UserDTO) -> UUID:
        return await self.repository.put_user(user)
    
    async def check_user(self, user: UserLogin) -> Tuple[bool, UUID]:
        return await user_repository.exists_by_full_name(user.first_name, user.last_name)
    
    async def get_all_users(self) -> List[UserDTO]:
        return await self.repository.get_all_users()
    
    async def get_user_by_id(self, id: str) -> UserDTO:
        return await self.repository.get_user_by_id(id)
    
    async def update_user_info(self, user: UserDTO, id: str) -> UserDTO:
        return await self.repository.update_user_info(
            id,
            first_name=user.first_name,
            last_name=user.last_name,
            sex=user.sex,
            birth_date=user.birth_date,
            current_position=user.current_position,
            education=user.education, 
            experience_years=user.experience_years, 
            experience_months=user.experience_months,
            experience_description=user.experience_description,
            hard_skills=user.hard_skills,
        )
    async def chat_llm(self, id, text_message):
        return await ai_service.process_message(user_id=id, message=text_message)

    async def start_chat_llm(self, id):
        ai_service.clear_history(user_id=id)
        user_info = await self.repository.get_user_by_id(id=id)
        user_info_one_line = "Ты hr помощник, твоя задача помочь человеку с выбором профессии, ты получишь о нем краткую информацию, помоги ему стать лучшим специалистом"
        user_info_one_line += await user_to_single_line(user_info)
        return await ai_service.process_message(user_id=id, message=user_info_one_line)
    
    async def generate_skills(self, id):
        ai_service.clear_history(user_id=id)
        user_info = await self.repository.get_user_by_id(id=id)
        user_info_one_line = """Ты hr помощник, твоя задача на основании резюме человека выделить следующие навыки: 1. Опыт (годы + месяцы)

1.1🎚 Уровень мастера — отражает суммарный опыт.

1.2 🕰 Выдержка — насколько стабильно и долго человек «в игре».

2. Текущее описание опыта / позиция

2.1 🛠 Фокус профессии — отражает специализацию (например: «Инженерный», «Аналитический», «Креативный»).

2.2 ⚡️ Скорость апгрейда — если видно, что часто менял роли/осваивал новое.

3. Стэк / хард-скиллы

3.1 🔧 Гибкость стэка — разнообразие навыков (один язык vs. много технологий).

3.2 🌐 Мультикласс — если стэк разный (например, и аналитика, и разработка).

4. Возраст / пол
Пол лучше не использовать для геймификации (может восприниматься как лишнее).
Возраст можно мягко отразить как:

4.1 ⏳ Опыт эпох — насколько «старый герой» по сравнению с «новичком».

генерировать ответ строго в формате json, поля следующие: 'level', 'discipline','focus', 'speed', 'flexibility', 'multiclass', 'experience'"""
        user_info_one_line += await user_to_single_line(user_info)
        answer = await ai_service.process_message(user_id=id, message=user_info_one_line)
        ai_service.clear_history(user_id=id)
        print(answer)
        return Skills(dict(answer))
        
user_service = UserService()
