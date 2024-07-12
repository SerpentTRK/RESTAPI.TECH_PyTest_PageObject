from pydantic import BaseModel
from typing import List, Optional

class Meta(BaseModel):
    total: int = 0
    limit: int = 0
    offset: int = 0

class Data(BaseModel):
    first_name: Optional[str]
    last_name: str
    company_id: int
    user_id: int

class ModelUsers200(BaseModel):
    meta: Optional[Meta]
    data: List[Data]