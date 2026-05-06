from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.repository import users
from blog.schema import (
    ForgotPasswordRequest,
    ReadUser,
    RestPasswordRequest,
    UserSchema,
    VerviyMessageModel,
)

user_router = APIRouter(
    tags=["user"],
    prefix="/user",
)


# crete new User


@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
# @limiter.limit("1/minute")
def create_user(
    request: Request,
    user: UserSchema,
    db: Session = Depends(get_db),
) -> dict:
    return users.create_user_new(user, db)


# return user with id
@user_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ReadUser)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    return users.get_user_exist(id, response, db)


@user_router.get(
    "/vervif/verify-email",
    status_code=status.HTTP_200_OK,
    response_model=VerviyMessageModel,
)
def verify_email(token: str, response: Response, db: Session = Depends(get_db)):
    return users.verify_email_rpeo(token, response, db)


@user_router.post("/forgot-password")
def forgot_password(
    request: Request, request1: ForgotPasswordRequest, db: Session = Depends(get_db)
):
    return users.forgot_password(request1.email, db)


@user_router.post("/rest/reset-password")
def reset_password(
    token: str, new_password: RestPasswordRequest, db: Session = Depends(get_db)
):
    return users.reset_password(token, new_password.password, db)
