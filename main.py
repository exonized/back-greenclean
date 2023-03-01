from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import fastapi.security as _security
import fastapi


import sqlalchemy.orm as _orm

import schemas.Users
import schemas.Categorie
import schemas.Produit
import schemas.Souscategorie
import schemas.Commandes
import schemas.UsersServices

import models
import config
from database import SessionLocal, engine

import Users.UsersDELETE
import Users.UsersGET
import Users.UsersPOST

import Users.UsersServiceDELETE
import Users.UsersServiceGET
import Users.UsersServicePOST

import Admin.AdminPOST
import Admin.AdminGET
import Admin.AdminDELETE

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"API GreenClean - G4"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Users

@app.post("/api/users", tags=["Utilisateur"])
async def create_user(
    user: schemas.Users.UserCreate, db: _orm.Session = fastapi.Depends(get_db)
):
    db_user = await Users.UsersGET.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(
            status_code=400, detail="Votre email est déjà utilisé")

    user = await Users.UsersPOST.create_user(user, db)

    return await Users.UsersPOST.create_token(user)


@app.post("/api/token", tags=["Utilisateur"])
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(get_db),
):
    user = await Users.UsersGET.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(
            status_code=401, detail="Utilisateur non enregistré")

    return await Users.UsersPOST.create_token(user)


@app.get("/api/users/me", tags=["Utilisateur"], response_model=schemas.Users.User)
async def get_user(user: schemas.Users.User = fastapi.Depends(Users.UsersGET.get_current_user)):
    return user


@app.delete("/api/user/me/delete", tags=["Utilisateur"])
async def delete_user(user: schemas.Users.User = fastapi.Depends(Users.UsersDELETE.delete_current_user)):
    return user


# UsersServices

@app.post("/api/services/users/", tags=["Services"])
async def create_user_services(
    user: schemas.UsersServices.UserServicesCreate, db: _orm.Session = fastapi.Depends(get_db)
):
    db_user = await Users.UsersServiceGET.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(
            status_code=400, detail="Votre email est déjà utilisé")

    user = await Users.UsersServicePOST.create_user(user, db)

    return await Users.UsersServicePOST.create_token(user)


@app.post("/api/services/token", tags=["Services"])
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(get_db),
):
    user = await Users.UsersServiceGET.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(
            status_code=401, detail="Utilisateur non enregistré")

    return await Users.UsersServicePOST.create_token(user)


@app.get("/api/services/me", tags=["Services"], response_model=schemas.UsersServices.UserServices)
async def get_user(user: schemas.UsersServices.UserServices = fastapi.Depends(Users.UsersServiceGET.get_current_user)):
    return user


@app.delete("/api/services/me/delete", tags=["Services"])
async def delete_user(user: schemas.UsersServices.UserServices = fastapi.Depends(Users.UsersServiceDELETE.delete_current_user)):
    return user


# Produits


@app.get("/api/get/produits", tags=["Produits"])
async def get_produits(prevention: schemas.Produit.Produits = fastapi.Depends(Users.UsersGET.get_produits)):
    return prevention


@app.get("/api/get/produits/{id}", tags=["Produits"])
async def get_produit_id(id: int, produit: schemas.Produit.Produits = fastapi.Depends(Users.UsersGET.get_produit_id)):
    return produit


@app.get("/api/get/produits/souscategorie/{produits}", tags=["Produits"])
async def get_produit_id(produits: str, produit: schemas.Produit.Produits = fastapi.Depends(Users.UsersGET.get_produit_produitname)):
    return produit


# Categories


@app.get("/api/get/categories", tags=["Categories"])
async def get_categories(categories: schemas.Categorie.Categories = fastapi.Depends(Users.UsersGET.get_categories)):
    return categories


@app.get("/api/get/souscategories/{categorie}", tags=["Categories"])
async def get_souscategorie_categories(categorie: schemas.Souscategorie.sousCategories = fastapi.Depends(Users.UsersGET.get_souscategories_categorie)):
    return categorie


# Commandes


@app.post("/api/commandes", tags=["Commandes"])
def commandes_create(produit: schemas.Commandes.Commandes = fastapi.Depends(Users.UsersPOST.create_commandes)):
    return produit


@app.get("/api/commandes/me", tags=["Commandes"])
async def get_commandes(user: schemas.Commandes.Commandes = fastapi.Depends(Users.UsersGET.get_current_commandes)):
    return user

# AdminPOST


@app.post("/api/produit", tags=["Admin-Produit"])
def produit_create(produit: schemas.Produit.Produits = fastapi.Depends(Admin.AdminPOST.create_produit)):
    return produit


@app.post("/api/categorie", tags=["Admin-Categorie"])
def categorie_create(categorie: schemas.Categorie.Categories = fastapi.Depends(Admin.AdminPOST.create_categorie)):
    return categorie


@app.post("/api/souscategorie", tags=["Admin-Categorie"])
def souscategorie_create(souscategorie: schemas.Souscategorie.sousCategories = fastapi.Depends(Admin.AdminPOST.create_souscategorie)):
    return souscategorie

# AdminGET


@app.get("/api/users/get", tags=["Admin-Utilisateur"], )
async def get_user_all(user: schemas.Users.User = fastapi.Depends(Admin.AdminGET.get_users)):
    return user


# AdminDELETE


@app.delete("/api/categorie/delete/{id}", tags=["Admin-Categorie"])
async def delete_categorie(id: int, categorie: schemas.Categorie.Categories = fastapi.Depends(Admin.AdminDELETE.delete_categorie)):
    return {"supprimer": categorie}
