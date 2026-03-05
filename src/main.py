from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get('/')
def index():
    # only get 10 published blogs
    return {'data': ' published blogs from the db'}
