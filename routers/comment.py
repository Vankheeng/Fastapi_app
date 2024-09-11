from fastapi import APIRouter, status, Depends
import repository.comment
import repository.group
import repository.member
from sqlalchemy.orm import Session
from database import get_db
import models
from oauth2 import get_current_user
import schemas.comment
from schemas.user import TokenData
from datetime import datetime
import repository, schemas

router = APIRouter(tags=['Comments'], prefix="/comments")

@router.post("", status_code=201)
def create_comment(request: schemas.comment.NewComment, current_user: TokenData = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return repository.comment.create_comment(request, current_user.username, db)

@router.put("", status_code=200)
def update_comment(request: schemas.comment.UpdateComment, current_user: TokenData = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return repository.comment.update_comment(request, current_user.username, db)

@router.delete("", status_code=200)
def delete_comment(comment_id: int , current_user: TokenData = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    return repository.comment.delete_comment(comment_id, current_user.username, db)

@router.get("", status_code=200)
def get_comment_of_blog(blog_id: int, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    return repository.comment.get_comment_of_blog(blog_id, current_user.username, db)