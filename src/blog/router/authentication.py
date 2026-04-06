from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.hashing import Hash
from blog.models import User
from blog.oauth2 import oauth
from blog.token import create_access_token, create_jwt
from blog.utils.jwt_blacklist import add_token_to_blacklist

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


# --- Endpoints ---
@auth_router.get("/login/{provider_name}")
async def login(provider_name: str, request: Request):
    client = getattr(oauth, provider_name, None)
    if not client:
        raise HTTPException(status_code=400, detail="Provider not supported")

    redirect_uri = request.url_for("auth_callback", provider_name=provider_name)
    print(request.url_for("auth_callback", provider_name="github"))
    return await client.authorize_redirect(request, redirect_uri)


@auth_router.get("/auth/{provider_name}/callback")
async def auth_callback(
    provider_name: str, request: Request, db: Session = Depends(get_db)
):
    client = getattr(oauth, provider_name, None)
    if not client:
        raise HTTPException(status_code=400, detail="Provider not supported")

    token = await client.authorize_access_token(request)

    # مثال Google
    if provider_name == "google":
        user_info = await client.parse_id_token(request, token)
        user_info["provider"] = "google"
    # مثال GitHub
    elif provider_name == "github":
        resp = await client.get("user", token=token)
        profile = resp.json()
        email_resp = await client.get("user/emails", token=token)
        emails = email_resp.json()
        primary_email = next((e["email"] for e in emails if e["primary"]), None)
        user_info = {
            "email": primary_email,
            "name": profile.get("name") or profile.get("login"),
            "provider": "github",
        }
        print("user github info ", user_info)
        user = db.query(User).filter(User.email == user_info["email"]).first()
        if not user:
            raise HTTPException(
                detail=f"no user with this email {user_info['email']} ",
                status_code=status.HTTP_404_NOT_FOUND,
            )

    jwt_token = create_jwt(user_info)
    return JSONResponse({"access_token": jwt_token, "user": user_info})
