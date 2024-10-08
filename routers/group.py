from fastapi import APIRouter, status, Depends
import repository.group
import repository.member
from schemas import group
from sqlalchemy.orm import Session
from database import get_db
import models, oauth2
import schemas.group
from schemas.user import TokenData
from datetime import datetime
import repository, schemas
router = APIRouter(tags=['Groups'], prefix="/groups")

@router.post("", status_code=status.HTTP_201_CREATED)
def create_group(request: group.CreateGroup, current_user: TokenData = Depends(oauth2.get_current_user), db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == current_user.username).first()
    repository.group.create_group(request, user.id, db)
    return {"Created group"}


@router.get('', status_code=200)
def find_group(groupname: str, db: Session = Depends(get_db),  current_user: TokenData = Depends(oauth2.get_current_user)):
    return repository.group.find_group(groupname, db)

@router.delete('', status_code=200)
def delete_group(groupname: str, db: Session = Depends(get_db),  current_user: TokenData = Depends(oauth2.get_current_user)):
    repository.group.delete_group(groupname, db, current_user)
    return {"Deleted"}

