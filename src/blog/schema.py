# from typing import Optional
from typing import List, Optional

from pydantic import BaseModel, EmailStr

# from typing import List


# class Blog(BaseModel):
#     title: str
#     body: str
#     published: Optional[bool]


# class User(BaseModel):
#     name: str
#     email: EmailStr
#     password:  str


# class ReadUser(BaseModel):
#     name: str
#     email: EmailStr
#     blogs: List[Blog]


# class ReadBlog(BaseModel):
#     title: str
#     body: str
#     creator: ReadUser

#     class Config():
#         from_attributes = True


#  Blog and User Schema
class BlogSChema(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    user_id: int

    class Config:
        orm_mode = True  # ← enable ORM mode


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class ReadUser(BaseModel):
    name: str
    email: EmailStr
    blogs: List[BlogSChema]

    class Config:
        orm_mode = True  # ← enable ORM mode


class ReadBlogSChema(BaseModel):
    title: str
    body: str
    creator: Optional[ReadUser]  # allow None if there is no creator

    class Config:
        orm_mode = True  # ← was `from_attributes` before, which is wrong


#  Authentication Schema
class UserLginSchema(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class RestPasswordRequest(BaseModel):
    password: str
