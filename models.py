from sqlalchemy import Column, Integer, String, TIMESTAMP
import passlib.hash as _hash
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "Utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    prenom = Column(String)
    nom = Column(String)
    adresse = Column(String)
    ville = Column(String)
    complement = Column(String)
    codepostal = Column(String)
    region = Column(String)
    numerorue = Column(String)
    roles = Column(String,  default=("Membre"))
    avatar = Column(String, default=(
        'https://greencleang4.s3.eu-west-3.amazonaws.com/Avatar/base.png'))
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class UserServices(Base):
    __tablename__ = "UtilisateursServices"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    siren = Column(String)
    roles = Column(String,  default=("Entreprise"))
    avatar = Column(String, default=(
        'https://greencleang4.s3.eu-west-3.amazonaws.com/Avatar/base.png'))
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Feedback(Base):
    __tablename__ = "Feedback"
    id = Column(Integer, primary_key=True, index=True)
    avatar_user = Column(String)
    id_user = Column(String)
    contenu = Column(String)
    etoile = Column(Integer)


class Commandes(Base):
    __tablename__ = "Commandes"
    id = Column(Integer, primary_key=True, index=True)
    produit = Column(String)
    numerocommandes = Column(String)
    user = Column(String)
    etat = Column(String, default=(
        'Votre commande est en cour de traitement...'))


class Categories(Base):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True, index=True)
    categorie = Column(String)
    images = Column(String)


class SousCategories(Base):
    __tablename__ = "SousCategories"
    id = Column(Integer, primary_key=True, index=True)
    souscategorie = Column(String)
    categorie = Column(String)
    images = Column(String)


class Produits(Base):
    __tablename__ = "Produits"
    id = Column(Integer, primary_key=True, index=True)
    produit = Column(String)
    description = Column(String)
    prix = Column(Integer)
    souscategories = Column(String)
    images = Column(String)


class Contact(Base):
    __tablename__ = "Contact"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    probleme = Column(String)
    message = Column(String)
    etat = Column(String,  default=('Non traité'))
    date = Column(TIMESTAMP(timezone=False),
                  nullable=False, default=datetime.now())


class Prevention(Base):
    __tablename__ = "Prevention"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    types = Column(String)
    description = Column(String)
    contenu = Column(String)
    images = Column(String)
    date = Column(TIMESTAMP(timezone=False),
                  nullable=False, default=datetime.now())


class Services(Base):
    __tablename__ = "Services"
    id = Column(Integer, primary_key=True, index=True)
    soustitre = Column(String)
    titre = Column(String)
    description = Column(String)
    images = Column(String)
