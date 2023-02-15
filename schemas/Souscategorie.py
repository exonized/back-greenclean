import pydantic as _pydantic


class _sousCategoriesBase(_pydantic.BaseModel):
    souscategorie: str
    categorie: str


class sousCategoriesCreate(_sousCategoriesBase):

    class Config:
        orm_mode = True


class sousCategories(_sousCategoriesBase):
    id: int
    images: str

    class Config:
        orm_mode = True
