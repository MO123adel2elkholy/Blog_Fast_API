from blog.database import engine, sessionlocal, get_db
from blog.models import Blog, User
from fastapi import FastAPI, Depends
from blog.schema import BlogSChema, ReadBlogSChema
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from typing import List
from blog.hashing import Hash
from fastapi import APIRouter


router = APIRouter()

blogschema = Blog


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: BlogSChema, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title,
                    body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# return all blogs
@router.get('/blogs', status_code=status.HTTP_200_OK, response_model=List[ReadBlogSChema], tags=['blogs'])
def all(db: Session = Depends(get_db)):
    return db.query(Blog).all()


# return blog with id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ReadBlogSChema, tags=['blogs'])
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return blog


# detlete bog with id
@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id: int, response: Response, db: Session = Depends(get_db)):
    db.query(Blog).filter(Blog.id ==
                          id).delete(synchronize_session=False)
    blog = db.commit()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return {"message": "succss"}


# update bog with id
@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id: int, request: ReadBlogSChema, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.query(Blog).filter(Blog.id == id).update(
            {'title': request.title, 'body': request.body}, synchronize_session=False)
        db.commit()

        return request
