import inspect

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from fastapi_cache import FastAPICache
from sqlalchemy import or_
from sqlalchemy.orm import Session

from blog.models import Blog
from blog.schema import BlogSChema

ALLOWED_SORT_FIELDS = {"id", "title", "created_at"}


# @router.get("/blog", response_model=PaginatedBlog)
# def get_blogs(
#     page: int = Query(1, ge=1),
#     size: int = Query(10, ge=1, le=100),
#     search: str | None = None,
#     sort_by: str = Query("id"),
#     order: str = Query("desc"),
#     db: Session = Depends(get_db),
# ):
#     query = db.query(Blog)

#     # 🔍 SEARCH
#     if search:
#         query = query.filter(
#             or_(Blog.title.ilike(f"%{search}%"), Blog.content.ilike(f"%{search}%"))
#         )

#     # 🔒 SAFE SORTING
#     if sort_by not in ALLOWED_SORT_FIELDS:
#         sort_by = "id"

#     column = getattr(Blog, sort_by)

#     if order == "desc":
#         query = query.order_by(column.desc())
#     else:
#         query = query.order_by(column.asc())

#     # 📊 TOTAL (قبل pagination)
#     total = query.count()

#     # 📄 PAGINATION
#     skip = (page - 1) * size
#     blogs = query.offset(skip).limit(size).all()

#     return {"page": page, "size": size, "total": total, "data": blogs}


def get_all_blogs(
    db: Session, page: int, size: int, search: str, sort_by: str, order: str
):
    query = db.query(Blog)

    # 🔍 SEARCH
    if search:
        query = query.filter(
            or_(Blog.title.ilike(f"%{search}%"), Blog.body.ilike(f"%{search}%"))
        )

    # 🔒 SAFE SORTING
    if sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "id"

    column = getattr(Blog, sort_by)

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    # 📊 TOTAL (قبل pagination)
    total = query.count()

    # 📄 PAGINATION
    skip = (page - 1) * size
    blogs = query.offset(skip).limit(size).all()

    return {"page": page, "size": size, "total": total, "data": blogs}

    # skip = (page - 1) * size
    # total = db.query(Blog).count()
    # blogs = db.query(Blog).offset(skip).limit(size).all()

    # return {"page": page, "size": size, "total": total, "data": blogs}


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
