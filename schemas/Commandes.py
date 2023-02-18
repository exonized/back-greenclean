import pydantic as _pydantic


class _CommandesBase(_pydantic.BaseModel):
    produit: str
    numerocommandes: str


class CommandesCreate(_CommandesBase):

    class Config:
        orm_mode = True


class Commandes(_CommandesBase):
    id: int
    user: str

    class Config:
        orm_mode = True
