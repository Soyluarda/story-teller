from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError

from api.auth import crud
from api.users import schema
from api.utils import constant


async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=constant.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, constant.SECRET_KEY, algorithm=constant.ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, constant.SECRET_KEY, algorithms=[constant.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        result = await crud.find_exists_user(username)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return schema.UserList(**result)

    except (PyJWTError, ValidationError):
        raise credentials_exception


def get_current_active_user(current_user: schema.UserList = Depends(get_current_user)):
    if current_user.status != "1":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
