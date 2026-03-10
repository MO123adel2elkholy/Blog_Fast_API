
from .database import engine
from . import models
from fastapi import FastAPI
from .router import blog, user, authentication

from .limiter import limiter, RateLimitExceeded, _rate_limit_exceeded_handler

models.Base.metadata.create_all(engine)


# …other imports…

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# limited using Slowapi (rate-limiting package )

# @app.get("/limited")
# @limiter.limit("1/minute")


app.include_router(blog.router)
app.include_router(user.user_router)
app.include_router(authentication.auth_router)
