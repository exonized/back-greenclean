import models
import fastapi
import jwt


import schemas.Users
import schemas.Commandes


import sqlalchemy.orm as _orm
from config import oauth2schema, JWT_SECRET
from db import get_db


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_user_by_id(id: str, db: _orm.Session):
    return db.query(models.User).filter(models.User.id == id).first()


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def get_current_user(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Mauvais email ou mot de passe"
        )

    return schemas.Users.User.from_orm(user)


async def get_produits(
    db: _orm.Session = fastapi.Depends(get_db),

):
    produits = db.query(models.Produits).filter().all()
    return produits


async def get_produit_id(
    id: int,
    db: _orm.Session = fastapi.Depends(get_db),
):
    produit = db.query(models.Produits).get(id)
    return (produit)


async def get_produit_souscategories(
    categorie: str,
    db: _orm.Session = fastapi.Depends(get_db),

):
    souscategorie = db.query(models.Produits).filter(
        models.Produits.souscategories == categorie).all()
    return (souscategorie)


async def get_produit_produitname(
    produits: str,
    db: _orm.Session = fastapi.Depends(get_db),

):
    produit = db.query(models.Produits).filter(
        models.Produits.souscategories == produits).all()
    return (produit)


async def get_categories(
    db: _orm.Session = fastapi.Depends(get_db),

):
    categories = db.query(models.Categories).filter().all()
    return categories


async def get_souscategories_categorie(
    categorie: str,
    db: _orm.Session = fastapi.Depends(get_db),

):
    souscategorie = db.query(models.SousCategories).filter(
        models.SousCategories.categorie == categorie).all()
    return (souscategorie)


async def get_current_commandes(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):

    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    membre = payload["email"]

    commandes = db.query(models.Commandes).filter(
        models.Commandes.user == membre).all()
    return (commandes)
