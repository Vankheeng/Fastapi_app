from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import CreateUser, UpdateUser
from models import User
from security.hashing import Hash
from security.validate_pw import valid_pw
from datetime import datetime

def create_user(request: CreateUser, db: Session = Depends(get_db)):
    db_username = db.query(User).filter(User.username == request.username).first()
    if valid_pw(request.password) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not a Valid Password ")
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail = "User with the username already exists.")
    # print(request)
    new_user=User(
        username=request.username,
        name = request.name,
        hashed_password=Hash.bcrypt(request.password),
        create_time = datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return request.password

def find_user(username:str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This username is not available")
    return user


def update(username: str, request: UpdateUser, db: Session = Depends(get_db)):
    if valid_pw(request.password) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not a Valid Password ")
        
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="this username doesn't exit"
        )
    if user:
        user.name = request.name
        user.hashed_password = Hash.bcrypt(request.password)

        db.commit()
    return user

