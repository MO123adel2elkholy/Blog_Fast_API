from sqladmin import Admin
from blog.database import engine
from .views import UserAdmin, BlogAdmin
from .auth import AdminAuth

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


def setup_admin(app):
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(SECRET_KEY)
    )

    admin.add_view(UserAdmin)
    admin.add_view(BlogAdmin)
