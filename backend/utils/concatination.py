from schemas.schemas import UserDTO
async def user_to_single_line(user: UserDTO) -> str:
    """Преобразует все поля UserDTO в одну строку"""
    parts = []
    
    if user.id:
        parts.append(f"id:{user.id}")
    
    parts.extend([
        f"first_name:{user.first_name}",
        f"last_name:{user.last_name}",
        f"sex:{user.sex.value}",
        f"birth_date:{user.birth_date}",
        f"current_position:{user.current_position}",
        f"education:{user.education or 'None'}",
        f"experience_years:{user.experience_years}",
        f"experience_months:{user.experience_months}",
        f"experience_total_months:{user.experience_total_months or 'None'}"
    ])
    
    if user.experience_description:
        parts.append(f"experience_description:{user.experience_description}")
    
    if user.hard_skills:
        parts.append(f"hard_skills:{','.join(user.hard_skills)}")
    
    if user.created_at:
        parts.append(f"created_at:{user.created_at}")
    
    if user.updated_at:
        parts.append(f"updated_at:{user.updated_at}")
    
    return " | ".join(parts)