
import sqlalchemy.orm as _orm

import jwt
import passlib.hash as _hash

from config import JWT_SECRET

import schemas.Users
import models


async def create_token(user: models.User):
    user_obj = schemas.Users.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer", roles=user.roles, email=user.email, id=user.id)


async def create_user(user: schemas.Users.UserCreate, db: _orm.Session):
    user_obj = models.User(
        email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password), prenom=user.prenom, nom=user.nom, adresse=user.adresse, complement=user.complement, codepostal=user.codepostal, region=user.region, numerorue=user.numerorue, ville=user.ville
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj
