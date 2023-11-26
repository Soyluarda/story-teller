from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserList(BaseModel):
    id: int = None
    email: str
    username: str
    created_on: Optional[datetime] = None
    status: str = None


class UserCreate(UserList):
    password: str
