from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from blog.Email.email import send_email
from blog.hashing import Hash
from blog.models import User
from blog.schema import UserSchema


def create_user_new(request: UserSchema, db: Session):
    # hashed_password = pwd_cxt.hash(request.password)

    new_user = User(
        name=request.name, password=Hash.bcrypt(request.password), email=request.email
    )
    user = db.query(User).filter(User.name == request.name).first()
    if user:
        raise HTTPException(
            detail=" user alerady found with this cridintial  ",
            status_code=status.HTTP_208_ALREADY_REPORTED,
        )
    else:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        send_email(
            "wlcome Email",
            "adel333mahmoud@gmail.com",
            f"Welcom {new_user} to Our blog  ",
        )

        return {"message": "Acount created Successfuly now you can login "}


def get_user_exist(id: int, response: Response, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            detail=f"no user with this id {id} ", status_code=status.HTTP_404_NOT_FOUND
        )

    return user
