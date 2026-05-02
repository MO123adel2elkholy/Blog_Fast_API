from fastapi import APIRouter, Depends, Query, status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from blog.database import get_db
from blog.limiter import limiter
from blog.oauth2 import get_current_user
from blog.repository import blogs
from blog.schema import BlogSChema, PaginatedBlog, ReadBlogSChema, UserSchema

router = APIRouter(
    tags=["blogs"],
    prefix="/blog",
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def create(
    request: Request,
    blog: BlogSChema,
    db: Session = Depends(get_db),
    get_current_user_auth: UserSchema = Depends(get_current_user),
):
    create_blog = blogs.create_blog(blog, db)
    await FastAPICache.clear("blogs")

    return create_blog


# return all blogs
@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedBlog)
@cache(expire=120, namespace="blogs")  # cache لمدة 60 ثانية
def all(
    db: Session = Depends(get_db),
    get_current_user_auth: UserSchema = Depends(get_current_user),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: str = "",
    sort_by: str = Query("id"),
    order: str = Query("desc"),
):
    print("Database HIt ")
    return blogs.get_all_blogs(db, page, size, search, sort_by, order)


# return blog with id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ReadBlogSChema)
def get_blog(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    get_current_user_auth: UserSchema = Depends(get_current_user),
):
    return blogs.get_blog_id(id, response, db)


# detlete bog with id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    get_current_user_auth: UserSchema = Depends(get_current_user),
):
    return blogs.delete_blog_id(id, response, db)


# update bog with id
@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_blog(
    id: int,
    request: BlogSChema,
    response: Response,
    db: Session = Depends(get_db),
    get_current_user_auth: UserSchema = Depends(get_current_user),
):
    return blogs.update_blog_id(id, request, response, db)
