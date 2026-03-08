from blog.database import get_db
from fastapi import Depends
from blog.schema import UserSchema, ReadUser
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import Response
from fastapi import APIRouter
from blog.repository import users

user_router = APIRouter(
    tags=['user'],
    prefix="/user",

)

# crete new User


@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=ReadUser)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    return users.create_user_new(request, db)


# return user with id
@user_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ReadUser)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    return users.get_user_exist(id, response, db)
