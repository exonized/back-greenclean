import fastapi.security as _security

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://gitlab.com/",
    "https://green-back.herokuapp.com/",
    "https://green-back.herokuapp.com/docs",
    "https://greenclean.vercel.app/"
]

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"


SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg'
}

S3_BUCKET_NAME = "greencleang4"
