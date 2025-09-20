from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime
from uuid import UUID
from dataclasses import dataclass
from typing import List, Optional

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

@dataclass
class ParsedResult:
    years_total_min: Optional[int]
    years_total_max: Optional[int]
    must_have: List[str]
    nice_to_have: List[str]
    