from repositories.db.user_repository import user_repository
from datetime import datetime
from fastapi import HTTPException

class UserService:
    def __init__(self):
        self.repository = user_repository
        
    async def put_user(self, first_name, last_name, sex, birth_date, current_position):
        try:
            try:
                birth_date_obj = datetime.strptime(birth_date, "%d.%m.%Y").date()
            except ValueError:
                try:
                    birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
                except ValueError:
                    try:
                        birth_date_obj = datetime.strptime(birth_date, "%d %m %Y").date()
                    except ValueError:
                        raise ValueError("Invalid date format. Use 'DD.MM.YYYY', 'YYYY-MM-DD' or 'DD MM YYYY'")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        user_id = await self.repository.put_user(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birth_date=birth_date_obj,
            current_position=current_position
        )
        return user_id
    async def update_user_info(self, id, education=None, experience_years=None, experience_months=None, experience_description=None, hard_skills=None):
        return await self.repository.update_user_info(id=id, education=education, experience_years=experience_years, experience_months=experience_months, experience_description=experience_description, hard_skills=hard_skills)
        