from fastapi import APIRouter, Depends, status, HTTPException
import database
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import User, TokenData, CreateUser, UpdateUser
import models, oauth2
from repository import user

router = APIRouter(
    prefix='/user',
    tags=['User']
)

get_db = database.get_db

@router.get('/', response_model=User)
def get_user(username:str, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return user.find_user(username, db)

@router.post("/create", status_code=200)
def create_user(request: CreateUser, db: Session = Depends(get_db)):
    user.create_user(request, db)
    return {"Created"}

@router.get('/me', response_model=User)
def get_user(db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return user.find_user(current_user.username, db)


@router.put("/update", response_model=User)
def update_user(request: UpdateUser, db: Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return user.update(current_user.username, request, db)


