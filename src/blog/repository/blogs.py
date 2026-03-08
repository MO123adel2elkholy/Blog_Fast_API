from blog.models import Blog, User
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from blog.schema import BlogSChema, ReadBlogSChema
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi import status


def get_all_blogs(db: Session):
    return db.query(Blog).all()


def create_blog(request: BlogSChema, db: Session):
    new_blog = Blog(title=request.title,
                    body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_blog_id(id: int, response: Response, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    return blog


def delete_blog_id(id: int, response: Response, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)

    else:
        db.query(Blog).filter(Blog.id == id).delete(
            synchronize_session=False)
        db.commit()
        return {"message": "succss"}


def update_blog_id(id: int, request: BlogSChema, response: Response, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.query(Blog).filter(Blog.id == id).update(
            {'title': request.title, 'body': request.body}, synchronize_session=False)
        db.commit()

        return request
