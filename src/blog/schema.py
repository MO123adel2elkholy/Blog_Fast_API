# from typing import Optional
# from pydantic import BaseModel, EmailStr
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


from typing import Optional, List
from pydantic import BaseModel, EmailStr


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    user_id: int

    class Config:
        orm_mode = True            # ← enable ORM mode


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class ReadUser(BaseModel):
    name: str
    email: EmailStr
    blogs: List[Blog]

    class Config:
        orm_mode = True            # ← enable ORM mode


class ReadBlog(BaseModel):
    title: str
    body: str
    creator: Optional[ReadUser]   # allow None if there is no creator

    class Config:
        orm_mode = True            # ← was `from_attributes` before, which is wrong
