import inspect

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi_cache import FastAPICache
from sqlalchemy.orm import Session

from blog.models import Blog
from blog.schema import BlogSChema

# @app.get("/products")
# def get_products(
#     page: int = 1,
#     size: int = 10,
#     db: Session = Depends(get_db)
# ):
#     skip = (page - 1) * size

#     total = db.query(Product).count()
#     products = db.query(Product).offset(skip).limit(size).all()

#     return {
#         "page": page,
#         "size": size,
#         "total": total,
#         "data": products
#     }


def get_all_blogs(db: Session, page: int, size: int):
    skip = (page - 1) * size
    total = db.query(Blog).count()
    blogs = db.query(Blog).offset(skip).limit(size).all()

    return {"page": page, "size": size, "total": total, "data": blogs}


def create_blog(request: BlogSChema, db: Session):
    new_blog = Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    print(inspect.iscoroutinefunction(FastAPICache.clear))

    return new_blog


def get_blog_id(id: int, response: Response, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND
        )

    return blog


def delete_blog_id(id: int, response: Response, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()

    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND
        )

    else:
        db.query(Blog).filter(Blog.id == id).delete(synchronize_session=False)
        db.commit()
        return {"message": "succss"}


def update_blog_id(id: int, request: BlogSChema, response: Response, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            detail=f"no blog with this id {id} ", status_code=status.HTTP_404_NOT_FOUND
        )
    else:
        db.query(Blog).filter(Blog.id == id).update(
            {"title": request.title, "body": request.body}, synchronize_session=False
        )
        db.commit()

        return request
