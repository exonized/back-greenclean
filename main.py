from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import models
import config
from database import SessionLocal, engine


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
