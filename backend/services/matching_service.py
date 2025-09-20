from repositories.db.vacancy_repository import VacancyRepository, vacancy_repository
from repositories.db.user_repository import UserRepository, user_repository
from matcher.config import MatcherConfig
from matcher.scorer import compute_match
from schemas.schemas import MatchResultDTO, MatchResult
from typing import List

cfg = MatcherConfig()

class MatchingService:
    def __init__(self, user_repository: UserRepository, vacancy_repository: VacancyRepository):
        self.user_repository = user_repository
        self.vacancy_repository = vacancy_repository

    async def match(self, user_id: str) -> List[MatchResultDTO]:
        vacs = await vacancy_repository.get_vacancy_list()
        user = await user_repository.get_user_by_id(user_id)
        
        results = []
        for vac in vacs:
            res = compute_match(user, vac, cfg)
            decision = _validate_res(res)
            dto = MatchResultDTO.model_validate(res)
            dto.decision = decision
            results.append(dto)
            
        return results
            
def _validate_res(res: MatchResult) -> bool:
    score = res.total
    if score >= 0.5:
        return True
    return False
    
matching_service = MatchingService(user_repository, vacancy_repository)