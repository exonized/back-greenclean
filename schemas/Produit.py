
import pydantic as _pydantic
from datetime import datetime


class _ProduitsBase(_pydantic.BaseModel):
    produit: str
    description: str
    prix: int
    souscategories: str


class ProduitsCreate(_ProduitsBase):

    class Config:
        orm_mode = True


class Produits(_ProduitsBase):
    id: int
    date: datetime
    images: str

    class Config:
        orm_mode = True
