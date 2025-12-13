from dotenv import load_dotenv
from fastapi import Header, HTTPException
from jose import jwt, JWTError
import os

load_dotenv()

SECRET = os.getenv("APP_JWT_SECRET")


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing auth header")

    token = authorization.split()[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])

        if payload["sub"] == "zasviat@gmail.com":
            return payload["sub"]
        raise HTTPException(403, "Not permitted")
    except JWTError:
        raise HTTPException(401, "Invalid token")
