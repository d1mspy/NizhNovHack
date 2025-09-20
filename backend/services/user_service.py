from uuid import UUID

from repositories.db.user_repository import user_repository
from schemas.schemas import UserDTO

class UserService:
    def __init__(self):
        self.repository = user_repository
        
    async def put_user(self, user: UserDTO) -> UUID:
        return await self.repository.put_user(user)
    
    async def update_user_info(self, user: UserDTO, id: str) -> UserDTO:
        return await self.repository.update_user_info(
            id, 
            education=user.education, 
            experience_years=user.experience_years, 
            experience_months=user.experience_months,
            experience_description=user.experience_description,
            hard_skills=user.hard_skills,
        )

user_service = UserService()