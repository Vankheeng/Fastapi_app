from fastapi import APIRouter, status, Depends
import repository.group
import repository.member
import repository.reaction
from schemas import group
from sqlalchemy.orm import Session
from database import get_db
import models
from oauth2 import get_current_user
import schemas.group
from schemas.user import TokenData
from datetime import datetime
import repository, schemas


router = APIRouter(tags=['Reactions'], prefix="/reactions")

@router.post("", status_code= 201)
def update_reaction(request: schemas.reaction.ReactionBase, current_user: TokenData = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    return repository.reaction.update_reaction(request, current_user.username, db)

@router.get("", status_code=200)
def get_reaction_of_blog(blog_id: int, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    return repository.reaction.get_reaction_of_blog(blog_id, current_user.username, db)
    