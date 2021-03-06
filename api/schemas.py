from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Role(str, Enum):
    admin = 'admin'
    user = 'user'


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str
    password: str


class User(UserBase):
    id: int
    username: str
    disabled: bool = False

    class Config:
        orm_mode = True


class UserInDB(User):
    password: str


class CommentBase(BaseModel):
    pass


class Comment(CommentBase):
    id: int
    date: datetime
    content: str
    id_user: int

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    content: str
