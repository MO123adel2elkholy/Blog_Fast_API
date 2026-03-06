
from .database import engine, sessionlocal
from . import models
from fastapi import FastAPI, Depends
from . import schema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
models.Base.metadata.create_all(engine)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# crete new blog
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# return all blogs
@app.get('/', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


# return bog with id
@app.get('/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return blog
