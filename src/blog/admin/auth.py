from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from blog.database import sessionlocal
from blog.models import User
from blog.hashing import Hash


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        db = sessionlocal()
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if not user:
            return False

        # if not Hash.verify(password, user.password):
        #     return False

        request.session.update({"user": user.email})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "user" in request.session
