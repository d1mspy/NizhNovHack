from fastapi import FastAPI, UploadFile, File, Path, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from uuid import UUID

from schemas.schemas import VacancyDTO, UserDTO
from services.parsing_service import ParsingService
from repositories.db.vacancy_repository import vacancy_repository
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

parsing_service = ParsingService(vacancy_repository)

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
    
@app.post("/chat/{id}")
async def chat(message:str, id: str = Path(...)) -> str:
    """
    удаление вакансии
    """
    answer = await user_service.chat_llm(id=id, text_message=message)
    if not answer:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="failed to give answer")
    return answer

@app.post("/start_chat/{id}")
async def start_chat(id: str = Path(...)) -> str:
    """
    удаление вакансии
    """
    answer = await user_service.start_chat_llm(id=id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="failed to start chat")
    return answer

@app.post("/register")
async def register(user: UserDTO) -> UUID:
    user_id = await user_service.put_user(user)
    return user_id

@app.patch("/user/update/{id}")
async def update_user_info(user: UserDTO, id: str = Path(...)) -> UserDTO:
    return await user_service.update_user_info(user, id)

@app.put("/{user_id}/matching")
async def match(user_id: str = Path(...)):
    results = await matching_service.match(user_id)
    return results