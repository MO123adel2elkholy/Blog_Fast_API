
from blog.models import User
from blog.schema import UserSchema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.exceptions import HTTPException

from blog.hashing import Hash
from fastapi.responses import Response


def create_user_new(request: UserSchema, db: Session):
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


def get_user_exist(id: int, response: Response, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            detail=f"no user with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return user
