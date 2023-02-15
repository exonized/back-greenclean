import pydantic as _pydantic


class _CategoriesBase(_pydantic.BaseModel):
    categorie: str


class CategoriesCreate(_CategoriesBase):

    class Config:
        orm_mode = True


class Categories(_CategoriesBase):
    id: int
    images: str

    class Config:
        orm_mode = True
