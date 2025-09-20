from fastapi import FastAPI, UploadFile, File, Path, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated

from schemas.schemas import VacancyDTO
from services.parsing_service import ParsingService
from repositories.db.vacancy_repository import VacancyRepository

app = FastAPI(title="Т1 хак",
              docs_url='/docs',
              redoc_url='/redoc',
              openapi_url='/openapi.json',
              root_path="/api"
            )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vac_repo = VacancyRepository()
parsing_service = ParsingService(vac_repo)

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
    