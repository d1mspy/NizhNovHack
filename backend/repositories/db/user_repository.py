from infrastructure.db.connect import pg_connection
from sqlalchemy import insert, select, update, delete
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from persistent.db.tables import User
from uuid import UUID

class UserRepository:
    def __init__(self)-> AsyncSession:
        self._sessionmaker = pg_connection()
    
    async def _execute_with_session(self, func, *args, **kwargs):
        async with self._sessionmaker() as session:
            try:
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except HTTPException:
                raise
            except Exception as e:
                await session.rollback()
                print(f"Database error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Database operation failed: {str(e)}"
                )
    async def put_user(self, first_name, last_name, sex, birth_date, current_position) -> UUID:
        async def _put(session: AsyncSession):
            try:
                birth_date_obj = datetime.strptime(birth_date, "%d %m %Y").date()
            except ValueError:
                try:
                    birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid date format. Use 'DD MM YYYY' or 'YYYY-MM-DD'"
                    )

            stmt = (
                insert(User)
                .values(
                    first_name = first_name,
                    last_name = last_name,
                    sex = sex,
                    birth_date=birth_date_obj,
                    current_position = current_position
                )
                .returning(User.id)
            )
            result = await session.execute(stmt)
            id = result.scalar_one()
            print(f"put user with id{id}")
            return id
        
        return await self._execute_with_session(_put)
    
    async def update_user_info(self, id, education=None, experience_years=None, experience_months=None, experience_description=None, hard_skills=None):
        async def _update(session: AsyncSession):
            stmt = update(User).values(education = education,
                                       experience_years = experience_years,
                                       experience_months = experience_months,
                                       experience_description = experience_description,
                                       hard_skills = hard_skills).where(User.id==id)
            result = await session.execute(stmt)    
            if result.rowcount > 0:
                return True
            else: return False
        return await self._execute_with_session(_update)

user_repository = UserRepository()