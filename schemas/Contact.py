import pydantic as _pydantic


class _ContactBase(_pydantic.BaseModel):
    probleme: str
    message: str


class ContactCreate(_ContactBase):

    class Config:
        orm_mode = True


class Contact(_ContactBase):
    id: int
    user: str
    etat: str
    date: str

    class Config:
        orm_mode = True
