from repositories.db.user_repository import user_repository
class UserService:
    def __init__(self):
        self.repository = user_repository
        
    async def put_user(self, first_name, last_name, sex, birth_date, current_position):
        return await self.repository.put_user(first_name=first_name, last_name=last_name, sex=sex, birth_date=birth_date, current_position=current_position)
    
    async def update_user_info(self, id, education=None, experience_years=None, experience_months=None, experience_description=None, hard_skills=None) -> bool:
        experience_years = int(experience_years)
        experience_months = int(experience_months)
        return await self.repository.update_user_info(id=id, education=education, experience_years=experience_years, experience_months=experience_months, experience_description=experience_description, hard_skills=hard_skills)

user_service = UserService()