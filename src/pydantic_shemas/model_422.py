from pydantic import BaseModel, field_validator
from typing import List, Any

from src.enums.schema_enums import Company_stats

class Ctx(BaseModel):
    expected: str

class DataFromDetail(BaseModel):
    type: str
    loc: list[str]
    msg: str
    input: Any  # любой тип данных
    url: str = None
    ctx: Ctx = None  # не обязательное поле

class Model422(BaseModel):
    detail: List[DataFromDetail]
