from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from blog.hashing import Hash
from blog.models import User
from blog.schema import UserSchema
from blog.token import create_vervication_token, verify_vemail_verification_token

# from celery_worker import welcome_email
from celery_worker import send_reset_email, send_verification_email

# from blog.tasks.sending_welcome_email import welcome_email


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

        # send_email(
        #     "wlcome Email",
        #     "adel333mahmoud@gmail.com",
        #     f"Welcom {new_user} to Our blog  ",
        # )
        print("Sendin Email --- ")
        token = create_vervication_token(new_user.email)
        send_verification_email.delay(to_email=new_user.email, token=token)

        # welcome_email.delay(
        #     "Welcome 🎉",
        #     "adel333mahmoud@gmail.com",
        #     f"Welcom {new_user.name} to Our blog 🚀",
        # )

        return {"message": "Acount created Successfuly now you can login "}


def get_user_exist(id: int, response: Response, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            detail=f"no user with this id {id} ", status_code=status.HTTP_404_NOT_FOUND
        )

    return user


def verify_email_rpeo(token: str, response: Response, db: Session):
    try:
        data = verify_vemail_verification_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )
    user = db.query(User).filter(User.email == data["sub"]).first()

    if not user:
        raise HTTPException(
            detail=f"no user with this Email {user.email} ",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    user.is_vervied = True
    db.commit()
    return {
        "message": "Email Vervied succesfuly Now you can Enjoying our website ",
        "status_code": status.HTTP_200_OK,
    }


def forgot_password(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(404, "User not found")

    token = create_vervication_token(email)

    send_reset_email.delay(email, token)

    return {"message": "Reset link sent"}


def reset_password(token: str, new_password: str, db: Session):

    try:
        data = verify_vemail_verification_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )

    # 2️⃣ تحقق من وجود المستخدم
    user = db.query(User).filter(User.email == data["sub"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 3️⃣ validation للباسورد
    if len(new_password) < 6:
        raise HTTPException(
            status_code=400, detail="Password must be at least 6 characters"
        )

    # 4️⃣ تحديث الباسورد
    user.password = Hash.bcrypt(new_password)

    # 🔐 (اختياري مهم) invalidate token
    # لو عندك column زي reset_token تمسحه هنا

    db.commit()
    return {"message": "Password updated"}
