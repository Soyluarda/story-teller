from fastapi import APIRouter, Depends, HTTPException
from api.auth.crud import find_exists_user, save_user, find_exist_user
from api.auth import schema
from api.utils import crypto
from api.utils import constant
from api.utils import jwt
from api.exceptions.exception import BaseException
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/auth/register", response_model=schema.UserList)
async def register(user: schema.UserCreate):
    result = await find_exists_user(user.email)
    if result:
        raise BaseException(status_code=400, detail="Email already exists.")


    user.password = crypto.hash_password(user.password)
    await save_user(user)
    return {**user.dict()}


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await find_exist_user(form_data.username)
    if not result:
        raise HTTPException(status_code=400, detail="User not found")

    user = schema.UserCreate(**result)
    verify_password = crypto.verify_password(form_data.password, user.password)
    if not verify_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = jwt.timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwt.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer",
            "user": {"email": user.email, "username": user.username}}
