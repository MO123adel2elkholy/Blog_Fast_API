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
from blog.repository import blogs


router = APIRouter(
    tags=['blogs'],
    prefix="/blog",

)

blogschema = Blog


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: BlogSChema, db: Session = Depends(get_db)):

    return blogs.create_blog(request, db)


# return all blogs
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ReadBlogSChema])
def all(db: Session = Depends(get_db)):
    return blogs.get_all_blogs(db)


# return blog with id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ReadBlogSChema)
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    return blogs.get_blog_id(id, response, db)


# detlete bog with id
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, response: Response, db: Session = Depends(get_db)):
    return blogs.delete_blog_id(id, response, db)


# update bog with id
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, )
def update_blog(id: int, request: BlogSChema, response: Response, db: Session = Depends(get_db)):
    return blogs.update_blog_id(id, request, response, db)
