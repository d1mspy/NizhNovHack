from repositories.db.vacancy_repository import VacancyRepository, vacancy_repository
from repositories.db.user_repository import UserRepository, user_repository
from matcher.config import MatcherConfig
from matcher.scorer import compute_match
from schemas.schemas import MatchResultDTO, MatchResult, UserDTO
from typing import List

cfg = MatcherConfig()

class MatchingService:
    def __init__(self, user_repository: UserRepository, vacancy_repository: VacancyRepository):
        self.user_repository = user_repository
        self.vacancy_repository = vacancy_repository

    async def match(self, user_id: str) -> List[MatchResultDTO]:
        vacs = await self.vacancy_repository.get_vacancy_list()
        user = await self.user_repository.get_user_by_id(user_id)
        
        results = []
        for vac in vacs:
            res = compute_match(user, vac, cfg)
            decision = _validate_res(res)
            dto = MatchResultDTO.model_validate(res)
            dto.decision = decision
            dto.vacancy = vac
            results.append(dto)
            
        return results
    
    async def vacancy_match(self, vac_id: str) -> List[MatchResultDTO]:
        users = await self.user_repository.get_all_users()
        vac = await self.vacancy_repository.get_vacancy_by_id(vac_id)
        
        results = []
        for user in users:
            res = compute_match(user, vac, cfg)
            decision = _validate_res(res)
            dto = MatchResultDTO.model_validate(res)
            dto.decision = decision
            dto.vacancy = vac
            dto.user_id = user.id
            results.append(dto)
            
        return results
    
    async def get_user_dict(self, user_id: str) -> dict:
        user = await user_repository.get_user_by_id(user_id)
        user_dict = user.to_plain_dict()
        return user_dict
            
def _validate_res(res: MatchResult) -> bool:
    score = res.score
    if score >= 0.5:
        return True
    return False
    
matching_service = MatchingService(user_repository, vacancy_repository)