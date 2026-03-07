
from .database import engine, sessionlocal
from . import models
from fastapi import FastAPI, Depends
from . import schema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from typing import List
from . import hashing


models.Base.metadata.create_all(engine)
Hashing = hashing.Hash()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# crete new blog
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# return all blogs
@app.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[schema.ReadBlog], tags=['blogs'])
def all(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


# return blog with id
@app.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.ReadBlog, tags=['blogs'])
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return blog


# detlete bog with id
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id: int, response: Response, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    blog = db.commit()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return {"message": "succss"}


# update bog with id
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id: int, request: schema.Blog, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.query(models.Blog).filter(models.Blog.id == id).update(
            {'title': request.title, 'body': request.body}, synchronize_session=False)
        db.commit()

        return request


# crete new User
@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schema.ReadUser, tags=['user'])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    # hashed_password = pwd_cxt.hash(request.password)

    new_user = models.User(name=request.name,
                           password=Hashing.bcrypt(request.password), email=request.email)
    user = db.query(models.User).filter(
        models.User.name == request.name).first()
    if user:
        raise HTTPException(
            detail=" user alerady found with this cridintial  ", status_code=status.HTTP_208_ALREADY_REPORTED)
    else:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return request


# return user with id
@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schema.ReadUser, tags=['user'])
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            detail=f"no user with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return user
