from fastapi import FastAPI, UploadFile, File, Path, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from uuid import UUID

from ai_services.matcher import analyzer
from schemas.schemas import VacancyDTO, UserDTO, UserLogin, MatchingResponse, Message
from services.parsing_service import parsing_service
from services.user_service import user_service
from services.matching_service import matching_service
from infrastructure.db.connect import sync_create_tables 

app = FastAPI(title="Т1 хак",
              docs_url='/docs',
              redoc_url='/redoc',
              openapi_url='/openapi.json',
              root_path="/api"
            )

user_service = user_service
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

@app.post("/vacancy")
async def add_vacancy(name: Annotated[str, Form(...)], vacancy: UploadFile = File(...)) -> VacancyDTO:
    """
    парсинг вакансии и добавление в базу данных
    """
    if not vacancy.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail=f"Только .pdf. Недопустим файл: {vacancy.filename}")
    
    vac_bytes = await vacancy.read()
    if not vac_bytes:
        raise HTTPException(status_code=400, detail="Файл пустой")
    
    dto = await parsing_service.add_vacancy(vac_bytes, name)
    return dto

@app.get("/vacancy")
async def get_vacancy_list() -> List[VacancyDTO]:
    """
    получение всех вакансий
    """
    data = await parsing_service.get_vacancy_list()
    return data

@app.delete("/vacancy/{id}")
async def delete_vacancy(id: str = Path(...)) -> None:
    """
    удаление вакансии
    """
    ok = await parsing_service.delete_vacancy(id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="failed to delete vacancy")

@app.put("/chat/{id}")
async def chat(message: Message, id: str = Path(...)) -> str:
    """
    отправка сообщений в чат
    """
    answer = await user_service.chat_llm(id=id, text_message=message.text)
    if not answer:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="failed to give answer")
    return answer

@app.put("/start_chat/{id}")
async def start_chat(id: str = Path(...)) -> str:
    """
    начало чата с моделькой
    """
    answer = await user_service.start_chat_llm(id=id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="failed to start chat")
    return answer

@app.get("/generate_skills_by_profile/{id}")
async def generate_skills(id: str = Path(...)):
    skills= await user_service.generate_skills(id=id)
    return skills
    

@app.get("/get_all_users")
async def get_all_users()->List[UserDTO]:
    """
    Возвращает список всех пользователей
    """
    answer = await user_service.get_all_users()
    return answer

@app.post("/register")
async def register(user: UserDTO) -> UUID:
    user_id = await user_service.put_user(user)
    return user_id

@app.post("/login")
async def login(user: UserLogin) -> UUID:
    data = await user_service.check_user(user)
    if not data[0]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exists")
    return data[1]

@app.patch("/user/update/{id}")
async def update_user_info(user: UserDTO, id: str = Path(...)) -> UserDTO:
    return await user_service.update_user_info(user, id)

@app.put("/{user_id}/matching")
async def match(user_id: str = Path(...)):
    results = await matching_service.match(user_id)
    resps = []
    for res in results:
        if res.decision:
            profile = await matching_service.get_user_dict(user_id)
            resp = await analyzer.match(
                user_profile=profile, 
                is_user=False, 
                vacancy=res.vacancy.description
            )
            feedback = MatchingResponse(
                score=resp.score,
                vac_name=res.vacancy.name,
                position=profile["current_position"],
                decision=resp.decision,
                reasoning_report=resp.reasoning_report
            )
            resps.append(feedback)
    
    return resps

@app.put("/vac/{vac_id}/matching")
async def match(vac_id: str = Path(...)):
    results = await matching_service.vacancy_match(vac_id)
    resps = []
    for res in results:
        if res.decision:
            profile = await matching_service.get_user_dict(res.user_id)
            resp = await analyzer.match(
                user_profile=profile, 
                is_user=False, 
                vacancy=res.vacancy.description
            )
            feedback = MatchingResponse(
                score=resp.score,
                position=profile["current_position"],
                decision=resp.decision,
                reasoning_report=resp.reasoning_report
            )
            resps.append(feedback)
    
    return resps

@app.get("/user/{id}")
async def get_user(id: str = Path(...)) -> UserDTO:
    return await user_service.get_user_by_id(id)
