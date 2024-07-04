from pydantic import BaseModel, field_validator
from typing import List

from src.enums.schema_enums import Company_stats


class Ctx(BaseModel):
    expected: str

class DataFromDetail(BaseModel):
    type: str
    loc: list[str]
    msg: str
    ctx: Ctx = None  # не обязательное поле

class ModelHttps422(BaseModel):
    detail: List[DataFromDetail]

