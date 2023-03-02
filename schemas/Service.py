
import pydantic as _pydantic
from datetime import datetime


class _ServiceBase(_pydantic.BaseModel):
    titre: str
    description: str
    soustitre: str


class ServiceCreate(_ServiceBase):

    class Config:
        orm_mode = True


class Service(_ServiceBase):
    id: int
    images: str

    class Config:
        orm_mode = True
