
from blog.database import Base, engine
from blog.typing import schema
from . import models
from fastapi import FastAPI
from .router import blog, user, authentication
from .limiter import limiter, RateLimitExceeded, _rate_limit_exceeded_handler
from ariadne.asgi import GraphQL


models.Base.metadata.create_all(engine)


# …other imports…


app = FastAPI(tilte='Blog Fsat Api')

app.add_route("/graphql", GraphQL(schema, debug=True))
app.add_websocket_route("/graphql", GraphQL(schema, debug=True))


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(blog.router)
app.include_router(user.user_router)
app.include_router(authentication.auth_router)
