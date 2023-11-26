import jwt
from jwt import PyJWTError
from pydantic import ValidationError
from datetime import datetime, timedelta
from api.utils import constant
from api.auth import schema
from api.auth import crud
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, constant.SECRET_KEY, algorithm=constant.ALGORITHM)

    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
    return encoded_jwt
    """


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, constant.SECRET_KEY, algorithms=[constant.ALGORITHM])
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
