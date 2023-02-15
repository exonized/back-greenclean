import sqlalchemy.orm as _orm
import fastapi
import jwt

from db import get_db
from config import oauth2schema, JWT_SECRET

import models


async def get_users(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),

):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    roles = payload["roles"]
    if (roles == "Admin"):
        users = db.query(models.User).filter().all()
    else:
        raise fastapi.HTTPException(
            status_code=409, detail="Vous n'êtes pas administrateur"
        )
    return users
