import fastapi.security as _security

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://gitlab.com/"
]

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"
