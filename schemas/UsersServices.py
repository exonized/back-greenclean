import pydantic as _pydantic


class _UserServicesBase(_pydantic.BaseModel):
    email: str
    siren: str


class UserServicesCreate(_UserServicesBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserServices(_UserServicesBase):
    id: int
    roles: str
    avatar: str

    class Config:
        orm_mode = True
