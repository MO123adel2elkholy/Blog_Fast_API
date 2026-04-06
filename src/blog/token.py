import os
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt

from blog.schema import TokenData

load_dotenv()
# base_dir = Path.resolve(self="__file__").parent.parent
# print(base_dir)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
print(str(SECRET_KEY), ALGORITHM)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
JWT_SECRET = os.getenv("SECRET_KEY")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Crreating Vervication token for Email Vervication


def create_vervication_token(email: str):  # or creating vervication  token
    expire = datetime.utcnow() + timedelta(minutes=5)
    pyload = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(pyload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(name=email)
    except JWTError:
        raise credentials_exception


def verify_vemail_verification_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


JWT_SECRET = os.getenv("SECRET_KEY")


# دالة مساعدة لإنشاء JWT
def create_jwt(user: dict):
    payload = {
        "sub": user["email"],
        "name": user.get("name"),
        "provider": user.get("provider"),
        "exp": time.time() + 3600,  # ساعة واحدة صلاحية
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
