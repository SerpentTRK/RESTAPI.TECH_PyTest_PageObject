from typing import List

from pydantic import BaseModel, field_validator, Field

from src.enums.schema_enums import Company_stats


"""
id: int   int = None или int = "" или int = 0 - если это не обязательный параметр
company_id: int = Field(gt=0) - Это вариант валидации инструментами pydantic, то же
самое что валидировано ниже
Для ключей с нижним подчеркиванием:
name: str Field(alias="_name")
"""
class Datum(BaseModel):
    company_id: int
    company_name: str
    company_address: str
    company_status: Company_stats  # аналог "enum": [ "ACTIVE", "CLOSED", "BANKRUPT"]

    @field_validator("company_id")
    def check_company_id(cls, company_id):
        """
        Прооверка Id компании. Число не может быть отрицательным
        Это пример того, что тут тоже можно проводить валидацию, создавая свои валидаторы
        """
        if company_id > 0:
            return company_id
        else:
            raise ValueError("Ошибка! Значение 'company_id' не может иметь отрицательного значения")

class Meta(BaseModel):
    limit: int
    offset: int
    total: int

class ModelCompanies200(BaseModel):
    data: List[Datum]
    meta: Meta


