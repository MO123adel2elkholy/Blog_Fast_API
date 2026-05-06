# # from sqladmin.authentication import AuthenticationBackend
# # from starlette.requests import Request

# # from blog.database import sessionlocal
# # from blog.hashing import Hash
# # from blog.models import User

# # hasing = Hash()


# # class AdminAuth(AuthenticationBackend):
# #     async def login(self, request: Request) -> bool:
# #         form = await request.form()
# #         name = form.get("username")
# #         password = form.get("password")

# #         db = sessionlocal()
# #         user = db.query(User).filter(User.name == name).first()
# #         db.close()
# #         # print("user ", user.username)
# #         if not user:
# #             print("No user with this cridintials ")
# #             return False

# #         if not Hash.verify(user.password, password):
# #             return False
# #         if not user.is_admin:
# #             print("Not admin user  ")
# #             return False

# #         request.session.update({"user": user.email})
# #         print("LOggd in User to system ")
# #         return True

# #     async def logout(self, request: Request) -> bool:
# #         request.session.clear()
# #         return True

# #     async def authenticate(self, request: Request) -> bool:
# #         return "user" in request.session


from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from blog.database import sessionlocal
from blog.hashing import Hash
from blog.models import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        name = form.get("username")
        password = form.get("password")

        db = sessionlocal()
        user = db.query(User).filter(User.name == name).first()
        db.close()

        if not user or not Hash.verify(user.password, password) or not user.is_admin:
            return False

        request.session.update({"user": user.email, "is_admin": user.is_admin})

        # prefer next from query params, then cookie, then session (consume session value)
        next_url = (
            request.query_params.get("next")
            or request.cookies.get("next")
            or request.session.pop("next", None)
        )
        redirect_to = next_url or "/admin"

        resp = RedirectResponse(url=redirect_to, status_code=302)
        resp.delete_cookie("next", path="/")
        return resp

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # allow sqladmin to continue; if there's a saved next cookie, let login handle it
        return "user" in request.session
