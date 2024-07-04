from typing import List

from pydantic import BaseModel, field_validator
from src.enums.schema_enums import Company_stats


class DescriptionLangItem(BaseModel):
    translation_lang: str
    translation: str

class ModelCompany200(BaseModel):
    company_id: int
    company_name: str
    company_address: str
    company_status: Company_stats
    # будет одно из двух:
    description: str = None
    description_lang: List[DescriptionLangItem] = None
