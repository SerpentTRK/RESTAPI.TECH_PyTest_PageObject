from pydantic import BaseModel
from typing import List, Optional

class Meta(BaseModel):
    total: int
    limit: int
    offset: int

class Data(BaseModel):
    first_name: Optional[str]
    last_name: str
    company_id: int
    user_id: int

class ModelUser200(BaseModel):
    meta: Meta
    data: List[Data]