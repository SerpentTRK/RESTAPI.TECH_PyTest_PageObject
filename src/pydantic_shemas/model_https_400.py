from pydantic import BaseModel


class Detail(BaseModel):
    reason: str

class Model400(BaseModel):
    detail: Detail