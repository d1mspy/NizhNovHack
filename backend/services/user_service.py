from uuid import UUID
from typing import Tuple

from repositories.db.user_repository import user_repository
from schemas.schemas import UserDTO, UserLogin
from ai_services.career import ai_service
from utils.concatination import user_to_single_line

class UserService:
    def __init__(self):
        self.repository = user_repository
        
    async def put_user(self, user: UserDTO) -> UUID:
        return await self.repository.put_user(user)
    
    async def check_user(self, user: UserLogin) -> Tuple[bool, UUID]:
        return await user_repository.exists_by_full_name(user.first_name, user.last_name)
    
    async def update_user_info(self, user: UserDTO, id: str) -> UserDTO:
        return await self.repository.update_user_info(
            id, 
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
        user_info_one_line = await user_to_single_line(user_info)
        return await ai_service.process_message(user_id=id, message=user_info_one_line)
    
user_service = UserService()
