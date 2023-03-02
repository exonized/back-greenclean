
import sqlalchemy.orm as _orm
import fastapi
import jwt
import passlib.hash as _hash
from fastapi import UploadFile, File
import magic
import boto3

from db import get_db
from config import oauth2schema, JWT_SECRET, SUPPORTED_FILE_TYPES, S3_BUCKET_NAME

import schemas.Produit
import schemas.Categorie
import schemas.Souscategorie

import models


async def create_produit(
    file: UploadFile = File(...),
    Produit: schemas.Produit.ProduitsCreate = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):

    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    roles = payload["roles"]

    if (roles == "Admin"):

        if not file:
            raise fastapi.HTTPException(
                status_code=fastapi.HTTPException(
                    status_code=400, detail="Fichier non trouvé..")
            )
        contents = await file.read()
        file_type = magic.from_buffer(buffer=contents, mime=True)

        if file_type not in SUPPORTED_FILE_TYPES:
            raise fastapi.HTTPException(
                status_code=400, detail="Le fromat de fichier n'est pas respecter"
            )

        s3 = boto3.resource('s3',
                            aws_access_key_id="AKIAUJ4KOY3EH3CM4H2I",
                            aws_secret_access_key="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")
        bucket = s3.Bucket(S3_BUCKET_NAME)
        await file.seek(0)

        bucket.upload_fileobj(
            file.file, file.filename)

        URL = "https://greencleang4.s3.eu-west-3.amazonaws.com/" + file.filename

        produit_obj = models.Produits(
            produit=Produit.produit, description=Produit.description, prix=Produit.prix, souscategories=Produit.souscategories, images=URL
        )
        db.add(produit_obj)
        db.commit()
        db.refresh(produit_obj)
    else:
        raise fastapi.HTTPException(
            status_code=409, detail="Vous n'êtes pas administrateur"
        )

    return (produit_obj)


async def create_categorie(
    file: UploadFile = File(...),
    Categorie: schemas.Categorie.CategoriesCreate = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):

    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    roles = payload["roles"]

    if (roles == "Admin"):

        if not file:
            raise fastapi.HTTPException(
                status_code=fastapi.HTTPException(
                    status_code=400, detail="Fichier non trouvé..")
            )
        contents = await file.read()
        file_type = magic.from_buffer(buffer=contents, mime=True)

        if file_type not in SUPPORTED_FILE_TYPES:
            raise fastapi.HTTPException(
                status_code=400, detail="Le fromat de fichier n'est pas respecter"
            )

        s3 = boto3.resource('s3',
                            aws_access_key_id="AKIAUJ4KOY3EH3CM4H2I",
                            aws_secret_access_key="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")
        bucket = s3.Bucket(S3_BUCKET_NAME)
        await file.seek(0)

        bucket.upload_fileobj(
            file.file, file.filename)

        URL = "https://greencleang4.s3.eu-west-3.amazonaws.com/" + file.filename

        categorie_obj = models.Categories(
            categorie=Categorie.categorie, images=URL
        )
        db.add(categorie_obj)
        db.commit()
        db.refresh(categorie_obj)
    else:
        raise fastapi.HTTPException(
            status_code=409, detail="Vous n'êtes pas administrateur"
        )

    return (categorie_obj)


async def create_souscategorie(
    file: UploadFile = File(...),
    sousCategorie: schemas.Souscategorie.sousCategoriesCreate = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):

    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    roles = payload["roles"]

    if (roles == "Admin"):

        if not file:
            raise fastapi.HTTPException(
                status_code=fastapi.HTTPException(
                    status_code=400, detail="Fichier non trouvé..")
            )
        contents = await file.read()
        file_type = magic.from_buffer(buffer=contents, mime=True)

        if file_type not in SUPPORTED_FILE_TYPES:
            raise fastapi.HTTPException(
                status_code=400, detail="Le fromat de fichier n'est pas respecter"
            )

        s3 = boto3.resource('s3',
                            aws_access_key_id="AKIAUJ4KOY3EH3CM4H2I",
                            aws_secret_access_key="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")
        bucket = s3.Bucket(S3_BUCKET_NAME)
        await file.seek(0)

        bucket.upload_fileobj(
            file.file, file.filename)

        URL = "https://greencleang4.s3.eu-west-3.amazonaws.com/" + file.filename

        souscategorie_obj = models.SousCategories(
            souscategorie=sousCategorie.souscategorie, categorie=sousCategorie.categorie,  images=URL
        )
        db.add(souscategorie_obj)
        db.commit()
        db.refresh(souscategorie_obj)
    else:
        raise fastapi.HTTPException(
            status_code=409, detail="Vous n'êtes pas administrateur"
        )

    return (souscategorie_obj)
