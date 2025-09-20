from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.user_service import UserService
from infrastructure.db.connect import sync_create_tables 

app = FastAPI(title="Т1 хак")

user_service = UserService()
sync_create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def test_endpoint() -> str:
    """
    тестовый эндпоинт
    """
    return "ok"

@app.post("/register")
async def register(first_name, last_name, sex, birth_date, current_position) -> int:#user_id
    user_id = await user_service.put_user(first_name, last_name, sex, birth_date, current_position)
    return user_id

@app.post("/update_user_info")
async def update_user_info(self, id, education=None, experience_years=None, experience_months=None, experience_description=None, hard_skills=None) -> int:
    user_id = await user_service.update_user_info(id=id, education=education, experience_years=experience_years, experience_months=experience_months, experience_description=experience_description, hard_skills=hard_skills)