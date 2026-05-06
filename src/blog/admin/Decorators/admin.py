# def admin_required(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         request: Request = kwargs.get("request")
#         user = request.session.get("user")
#         if not user or not user.get("is_admin"):
#             raise HTTPException(status_code=403)
#         return await func(*args, **kwargs)
#     return wrapper
from fastapi import HTTPException, Request
from fastapi.exceptions import HTTPException
from fastapi.requests import Request


def admin_required(request: Request):

    user = request.session.get("user")

    print(f"user seesion Data => {user}")

    if not user:
        raise HTTPException(status_code=401)

    if not user.get("is_admin"):
        raise HTTPException(status_code=403)

    return user
