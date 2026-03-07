from blog.database import engine, sessionlocal, get_db
from blog.models import Blog, User
from fastapi import FastAPI, Depends
from blog.schema import BlogSChema, ReadBlogSChema, UserSchema, ReadUser
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from typing import List
from blog.hashing import Hash
from fastapi import APIRouter

user_router = APIRouter()

# crete new User


@user_router.post('/user', status_code=status.HTTP_201_CREATED, response_model=ReadUser, tags=['user'])
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    # hashed_password = pwd_cxt.hash(request.password)

    new_user = User(name=request.name,
                    password=Hash.bcrypt(request.password), email=request.email)
    user = db.query(User).filter(
        User.name == request.name).first()
    if user:
        raise HTTPException(
            detail=" user alerady found with this cridintial  ", status_code=status.HTTP_208_ALREADY_REPORTED)
    else:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return request


# return user with id
@user_router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=ReadUser, tags=['user'])
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            detail=f"no user with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return user
