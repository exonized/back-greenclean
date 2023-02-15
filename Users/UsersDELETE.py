
import sqlalchemy.orm as _orm
import fastapi
import jwt

from db import get_db
from config import oauth2schema, JWT_SECRET

import schemas.Users
import models


async def delete_current_user(
    db: _orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
        db.delete(user)
        db.commit()

    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Problème lors de la suppression"
        )

    return schemas.Users.User.from_orm(user)
