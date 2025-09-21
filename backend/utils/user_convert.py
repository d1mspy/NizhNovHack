from typing import Dict
from schemas.schemas import UserDTO

def update_user_from_analysis(user: UserDTO, analysis_dict: Dict) -> UserDTO:
    """
    обновляет объект UserDTO на основе словаря, возвращённого ai_service.analyze_dialog.
    """
    if "experience_description" in analysis_dict:
        user.experience_description = analysis_dict["experience_description"]

    if "hard_skills" in analysis_dict:
        user.hard_skills = analysis_dict["hard_skills"]

    return user
