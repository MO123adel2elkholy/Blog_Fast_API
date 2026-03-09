from blog.database import get_db
from fastapi import Depends
from blog.schema import UserLginSchema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import Response
from fastapi import APIRouter
from blog.repository import users
from blog.models import User
from fastapi.exceptions import HTTPException
from blog.hashing import Hash
from blog.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
auth_router = APIRouter(
    tags=['auth'],
)

# crete new User


@auth_router.post('/login', status_code=status.HTTP_200_OK)
def create_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
