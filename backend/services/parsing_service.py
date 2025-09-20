from typing import List

from repositories.db.vacancy_repository import VacancyRepository
from utils.docx_extract import pdf_to_txt_via_docx
from utils.txt_parse import parse_vacancy_text
from schemas.schemas import VacancyDTO

class ParsingService():
    def __init__(self, repository: VacancyRepository):
        self.repository = repository
    
    async def add_vacancy(self, vacancy: bytes, name: str) -> VacancyDTO | None:
        vac_txt = await pdf_to_txt_via_docx(vacancy)
        res = parse_vacancy_text(vac_txt)
        
        min_months = None
        max_months = None
        
        if res.years_total_min != None:
            min_months = res.years_total_min*12
        if res.years_total_max != None:
            max_months = res.years_total_max*12
        
        dto = VacancyDTO(
            name=name,
            description=vac_txt,
            min_exp_months=min_months,
            max_exp_months=max_months,
            must_have=res.must_have,
            nice_to_have=res.nice_to_have
        )
        
        await self.repository.add_vacancy(dto)
        
        return dto
    
    async def get_vacancy_list(self) -> List[VacancyDTO]:
        data = await self.repository.get_vacancy_list()
        return data
    
    async def delete_vacancy(self, id: str) -> bool:
        ok = await self.repository.delete_vacancy(id)
        return ok