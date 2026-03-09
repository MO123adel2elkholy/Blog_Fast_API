
from .database import engine
from . import models
from fastapi import FastAPI
from .router import blog, user, authentication


models.Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(blog.router)
app.include_router(user.user_router)
app.include_router(authentication.auth_router)
