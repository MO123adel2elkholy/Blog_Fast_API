from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
from . import schema

app = FastAPI()


@app.post('/blog')
def index(blog: schema.Blog):
    # only get 10 published blogs
    return blog
