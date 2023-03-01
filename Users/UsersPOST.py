
import sqlalchemy.orm as _orm

import jwt
import passlib.hash as _hash

import fastapi
from db import get_db
from config import oauth2schema
from config import JWT_SECRET


import schemas.Users
import schemas.Commandes
import schemas.Contact
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


async def create_commandes(
    Commandes: schemas.Commandes.CommandesCreate = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    membre = payload["email"]

    commandes_obj = models.Commandes(
        produit=Commandes.produit, numerocommandes=Commandes.numerocommandes, user=membre
    )
    db.add(commandes_obj)
    db.commit()
    db.refresh(commandes_obj)

    return (commandes_obj)


async def create_contact(
    Contact: schemas.Contact.ContactCreate = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    membre = payload["email"]

    contact_obj = models.Contact(
        probleme=Contact.probleme, message=Contact.message, user=membre
    )
    db.add(contact_obj)
    db.commit()
    db.refresh(contact_obj)

    return (contact_obj)
