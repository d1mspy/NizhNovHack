from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional, Union, List, Dict
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.db.connect import pg_connection
from persistent.db.tables import User
from schemas.schemas import UserDTO
from utils.uuid import normalize_uuid

class UserRepository:
    def __init__(self) -> None:
        self._sessionmaker: async_sessionmaker[AsyncSession] = pg_connection()

    async def _execute_with_session(
        self,
        func: Callable[[AsyncSession], Awaitable[Any]],
    ) -> Any:
        async with self._sessionmaker() as session:
            try:
                result = await func(session)
                await session.commit()
                return result
            except HTTPException:
                await session.rollback()
                raise
            except Exception as e:
                await session.rollback()
                print(f"Database error: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Database operation failed: {str(e)}"
                )

    async def put_user(self, user: UserDTO) -> UUID:
        """
        вставляет пользователя и возвращает его id.
        """
        async def _put(session: AsyncSession) -> UUID:
            stmt = (
                insert(User)
                .values(**user.to_create_kwargs())
                .returning(User.id)
            )
            result = await session.execute(stmt)
            new_id: UUID = result.scalar_one()
            return new_id

        return await self._execute_with_session(_put)

    async def put_user_returning_dto(self, user: UserDTO) -> UserDTO:
        """
        вставляет пользователя и возвращает полностью заполненный DTO
        """
        async def _put(session: AsyncSession) -> UserDTO:
            stmt = (
                insert(User)
                .values(**user.to_create_kwargs())
                .returning(*User.__table__.columns)
            )
            row = (await session.execute(stmt)).mappings().one()
            return UserDTO.model_validate(dict(row))

        return await self._execute_with_session(_put)

    async def update_user_info(
        self,
        id: Union[UUID, str],
        *,
        education: Optional[str] = None,
        experience_years: Optional[int] = None,
        experience_months: Optional[int] = None,
        experience_description: Optional[str] = None,
        hard_skills: Optional[List[str]] = None,
    ) -> UserDTO:
        """
        частичное обновление. Обновляются только поля, переданные не None
        возвращает обновлённый UserDTO, если пользователь не найден — 404.
        """
        async def _update(session: AsyncSession) -> UserDTO:
            vid = normalize_uuid(id)
            values: Dict[str, Any] = {}

            if education is not None:
                values["education"] = education
            if experience_years is not None:
                values["experience_years"] = experience_years
            if experience_months is not None:
                values["experience_months"] = experience_months
            if experience_description is not None:
                values["experience_description"] = experience_description
            if hard_skills is not None:
                values["hard_skills"] = hard_skills

            if not values:
                stmt = (
                    update(User)
                    .where(User.id == vid)
                    .values({})
                    .returning(*User.__table__.columns)
                )
            else:
                stmt = (
                    update(User)
                    .where(User.id == vid)
                    .values(**values)
                    .returning(*User.__table__.columns)
                )

            result = await session.execute(stmt)
            row = result.mappings().one_or_none()
            if row is None:
                raise HTTPException(status_code=404, detail="User not found")

            return UserDTO.model_validate(dict(row))

        return await self._execute_with_session(_update)
    
    async def get_user(self, id):
        async def _get(session:AsyncSession) -> UserDTO:
            stmt = select(User).where(User.id==id)
    
    
user_repository = UserRepository()