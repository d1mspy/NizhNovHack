import enum
from sqlalchemy import (
    Column, Text, Date, Integer, SmallInteger, CheckConstraint, Computed, text
)
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlalchemy.sql import quoted_name

from persistent.db.base import Base, WithId, With_created_at, With_updated_at

class SexEnum(enum.Enum):
    male = "male"
    female = "female"

class User(Base, WithId, With_created_at, With_updated_at):
    __tablename__ = quoted_name("user", True)

    first_name = Column(Text, nullable=False)
    last_name  = Column(Text, nullable=False)

    # пол — нативный PG ENUM
    sex = Column(ENUM(SexEnum, name="sex_enum", create_type=False), nullable=False)

    birth_date = Column(Date, nullable=False)
    
    current_position = Column(Text, nullable=False)

    # доп. поля
    education = Column(Text)
    experience_years  = Column(SmallInteger, nullable=False, server_default=text("0"))
    experience_months = Column(SmallInteger, nullable=False, server_default=text("0"))

    # генерируемое поле
    experience_total_months = Column(
        Integer,
        Computed("experience_years * 12 + experience_months", persisted=True),
        nullable=False,
    )

    experience_description = Column(Text)

    hard_skills = Column(ARRAY(Text), nullable=False, server_default=text("ARRAY[]::text[]"))

    __table_args__ = (
        CheckConstraint("btrim(first_name) <> '' AND char_length(first_name) <= 50",
                        name="ck_user_first_name"),
        CheckConstraint("btrim(last_name) <> '' AND char_length(last_name) <= 50",
                        name="ck_user_last_name"),
        CheckConstraint("birth_date <= CURRENT_DATE AND birth_date > CURRENT_DATE - INTERVAL '120 years'",
                        name="ck_user_birth_date"),
        CheckConstraint("current_position ~ '[^[:space:]]'",
                        name="ck_user_current_position"),
        CheckConstraint("experience_years >= 0 AND experience_years <= 80",
                        name="ck_user_experience_years"),
        CheckConstraint("experience_months BETWEEN 0 AND 11",
                        name="ck_user_experience_months"),
        {"extend_existing": True},
    )
    
class Vacancy(Base, WithId, With_created_at, With_updated_at):
    __tablename__ = "vacancy"
    
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    
    min_exp_months = Column(SmallInteger, nullable=True)
    max_exp_months = Column(SmallInteger, nullable=True)
    
    must_have = Column(ARRAY(Text), nullable=False, server_default=text("'{}'::text[]"))
    nice_to_have = Column(ARRAY(Text), nullable=False, server_default=text("'{}'::text[]"))

    __table_args__ = tuple(
        CheckConstraint(
            "(min_exp_months IS NULL) OR (max_exp_months IS NULL) "
            "OR (min_exp_months <= max_exp_months)",
            name="vacancy_min_max_check",
        )
    )