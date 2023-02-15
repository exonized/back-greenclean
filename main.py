from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import fastapi.security as _security
import fastapi


import sqlalchemy.orm as _orm

import schemas.Users
import models
import config
from database import SessionLocal, engine

import Users.UsersDELETE
import Users.UsersGET
import Users.UsersPOST

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
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


# Users
