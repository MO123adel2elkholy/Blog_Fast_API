from typing import Optional
from pydantic import BaseModel, EmailStr


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class ReadBlog(BaseModel):
    title: str
    body: str

    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: EmailStr
    password:  str


class ReadUser(BaseModel):
    name: str
    email: EmailStr
