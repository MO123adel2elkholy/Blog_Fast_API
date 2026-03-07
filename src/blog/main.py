
from .database import engine, sessionlocal, get_db
from . import models
from fastapi import FastAPI, Depends
from . import schema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from typing import List
from . import hashing
from .router import blog, user


models.Base.metadata.create_all(engine)
Hashing = hashing.Hash()


app = FastAPI()

app.include_router(blog.router)
app.include_router(user.user_router)


# crete new blog
# @app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
# def create(request: schema.Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title=request.title,
#                            body=request.body, user_id=request.user_id)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog
