from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class userCreate(BaseModel):
    email: EmailStr
    password: str


class userOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class token(BaseModel):
    access_token: str
    token_type: str


class tokenData(BaseModel):
    id: Optional[int] = None
