from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator
from datetime import datetime, date
from uuid import UUID
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Any
import enum

class VacancyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # allow ORM -> DTO

    id: Optional[UUID] = None
    name: str
    description: str
    min_exp_months: Optional[int] = None
    max_exp_months: Optional[int] = None
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @model_validator(mode="after")
    def _check_exp(self):
        if self.min_exp_months is not None and self.max_exp_months is not None:
            if self.min_exp_months > self.max_exp_months:
                raise ValueError("min_exp_months cannot be greater than max_exp_months")
        return self
    

class Skills(BaseModel):
    level: Optional[int] = None
    discipline: Optional[int] = None
    focus: Optional[int] = None
    speed: Optional[int] = None
    flexibility: Optional[int] = None
    multiclass: Optional[int] = None
    experience: Optional[int] = None
    
    
class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: Optional[UUID] = None

    first_name: str
    last_name: str
    sex: SexEnum
    birth_date: date
    current_position: str

    education: Optional[str] = None
    experience_years: int = 0
    experience_months: int = 0
    # генерируемое поле: читаем как Optional, но не передаём при INSERT
    experience_total_months: Optional[int] = None

    experience_description: Optional[str] = None
    hard_skills: List[str] = Field(default_factory=list)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # приведения/валидации

    @field_validator("sex", mode="before")
    @classmethod
    def _coerce_sex(cls, v: Union[str, SexEnum]) -> SexEnum:
        if isinstance(v, str):
            vs = v.strip().lower()
            if vs in ("male", "female"):
                return SexEnum(vs)
        return v

    @field_validator("first_name", "last_name", "current_position")
    @classmethod
    def _strip_and_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be empty or whitespace-only")
        return v

    @field_validator("hard_skills", mode="before")
    @classmethod
    def _none_to_list(cls, v):
        return [] if v is None else v

    # проверка корректности переданных полей
    @model_validator(mode="after")
    def _business_rules(self):
        today = date.today()
        oldest = date(today.year - 120, today.month, today.day)
        if not (oldest < self.birth_date <= today):
            raise ValueError("birth_date must be within last 120 years and not in the future")

        if not (0 <= self.experience_years <= 80):
            raise ValueError("experience_years must be between 0 and 80")

        if not (0 <= self.experience_months <= 11):
            raise ValueError("experience_months must be between 0 and 11")

        # Для удобства вычислим локально, если БД ещё не вернула значение
        if self.experience_total_months is None:
            self.experience_total_months = self.experience_years * 12 + self.experience_months

        return self

    # хэлпер для вставки в таблицу
    def to_create_kwargs(self) -> dict:
        """
        Поля для INSERT в таблицу user.
        Исключаем id, created_at/updated_at и
        вычисляемое experience_total_months.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "sex": self.sex,
            "birth_date": self.birth_date,
            "current_position": self.current_position,
            "education": self.education,
            "experience_years": self.experience_years,
            "experience_months": self.experience_months,
            "experience_description": self.experience_description,
            "hard_skills": self.hard_skills,
        }
        
    def to_plain_dict(
        self,
        *,
        exclude_none: bool = False,
        json_mode: bool = True,
        by_alias: bool = False,
    ) -> dict:
        """
        словарь без служебных полей
        json_mode=True -> enum в строки, даты в ISO
        """
        exclude = {"id", "created_at", "updated_at", "experience_total_months"}
        return self.model_dump(
            exclude=exclude,
            exclude_none=exclude_none,
            by_alias=by_alias,
            mode="json" if json_mode else "python",
        )
        
class MatchResultDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str | None = None
    decision: bool = False
    vacancy: VacancyDTO | None = None
    score: float = Field(..., ge=0.0, le=1.0, description="Aggregated score in [0,1]")
    breakdown: Dict[str, float] = Field(default_factory=dict, description="Per-metric scores in [0,1]")
    details: Dict[str, Any] = Field(default_factory=dict, description="Debug/trace info (matches, tokens, etc.)")

    @model_validator(mode="after")
    def _check_breakdown(self):
        for k, v in (self.breakdown or {}).items():
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"breakdown[{k}] must be in [0,1], got {v}")
        return self
    
class UserLogin(BaseModel):
    first_name: str
    last_name: str
    
class MatchingResponse(BaseModel):
    score: int
    position: str
    decision: str
    reasoning_report: str
    
class Message(BaseModel):
    text: str
    
class SexEnum(enum.Enum):
    male = "male"
    female = "female"

@dataclass
class ParsedResult:
    years_total_min: Optional[int]
    years_total_max: Optional[int]
    must_have: List[str]
    nice_to_have: List[str]
    
@dataclass
class MatchResult:
    score: float
    breakdown: Dict[str, float]
    details: Dict[str, Any]