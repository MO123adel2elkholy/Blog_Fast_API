
from .database import engine
from . import models
from fastapi import FastAPI


from . import schema, database, models

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.post('/blog')
def index(blog: schema.Blog):
    # only get 10 published blogs
    return blog
