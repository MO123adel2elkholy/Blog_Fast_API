from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.hashing import Hash
from blog.models import User
from blog.token import create_access_token
from blog.utils import add_token_to_blacklist

auth_router = APIRouter(
    tags=["auth"],
)

# crete new User


router = APIRouter()


@auth_router.post("/logout")
def logout(authorization: str = Header(...)):
    token = authorization.split(" ")[1]  # "Bearer <token>"

    # ضيف التوكن للـ blacklist
    add_token_to_blacklist(token)

    return {"message": "Logged out successfully"}


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def create_user(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.name == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
