from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Union
from uuid import UUID

from persistent.db.tables import Vacancy
from infrastructure.db.connect import pg_connection
from schemas.schemas import VacancyDTO
from utils.uuid import normalize_uuid

class VacancyRepository:
    def __init__(self):
        self._sessionmaker = pg_connection()
        
    async def add_vacancy(self, dto: VacancyDTO) -> None:
        async with self._sessionmaker() as session:
            obj = Vacancy(
                name=dto.name,
                description=dto.description,
                min_exp_months=dto.min_exp_months,
                max_exp_months=dto.max_exp_months,
                must_have=dto.must_have or [],
                nice_to_have=dto.nice_to_have or [],
            )
            session.add(obj)
            await session.commit()
                
    async def get_vacancy_list(self) -> List[VacancyDTO]:
        stmp = select(Vacancy).order_by(Vacancy.created_at.desc())
        async with self._sessionmaker() as session:
            result = await session.execute(stmp)
            vacancies: list[Vacancy] = result.scalars().all()

        return [VacancyDTO.model_validate(v) for v in vacancies]
            
    async def delete_vacancy(self, id: Union[str, UUID]) -> bool:
        vid = normalize_uuid(id)
        
        stmt = delete(Vacancy).where(Vacancy.id == vid).returning(Vacancy.id)

        async with self._sessionmaker() as session:
            try:
                res = await session.execute(stmt)
                ok = res.scalar_one_or_none() is not None
                if ok:
                    await session.commit()
                else:
                    await session.rollback()
                return ok
            except IntegrityError:
                await session.rollback()
                raise