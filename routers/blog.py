from fastapi import APIRouter, Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from repository import user
import repository.blog
import models, schemas, repository
import schemas.blog
from schemas.user import TokenData
from typing import List




router = APIRouter(
    prefix="/Blog",
    tags=['Blogs']
)


@router.post('', status_code=200)
def create_blog(request: schemas.blog.CreateBlog, current_user: TokenData = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return repository.blog.create_blog(request, current_user.username, db)

@router.get("", status_code=200)
def get_blogs(group_name: str = Depends, current_user: TokenData = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return repository.blog.get_blogs(group_name, current_user.username, db)

@router.get("/get_blog_of_user", status_code=200)
def get_blogs_of_user(request: schemas.blog.GetBlog, current_user: TokenData = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return repository.blog.get_blogs(request, current_user.username, db)

@router.get("/get_waiting_blogs", status_code=200)
def get_waiting_blogs(group_name: str = Depends, current_user: TokenData = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return repository.blog.get_waiting_blogs(group_name, current_user.username, db)

@router.put("", status_code=200)
def accept_blog(request:schemas.blog.AcceptBlog, current_user: TokenData = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    return repository.blog.accept_blog(request, current_user.username, db)

@router.delete("", status_code=200)
def delete_blog(blog_id: int, current_user: TokenData = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return repository.blog.delete_blog(blog_id, current_user.username, db)