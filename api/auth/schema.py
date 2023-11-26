from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserList(BaseModel):
    id: int = None
    email: str
    username: str
    created_on: Optional[datetime] = None
    status: str = None

class SocialUser(UserList):
    social_auth: str


class UserCreate(UserList):
    password: str
