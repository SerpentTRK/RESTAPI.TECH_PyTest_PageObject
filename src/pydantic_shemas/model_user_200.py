from pydantic import BaseModel
from typing import List, Optional

class ModelUser200(BaseModel):
    first_name: str
    last_name: str
    company_id: int
    user_id: int
