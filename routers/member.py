from fastapi import APIRouter, status, Depends
import repository.group
import repository.member
from schemas import group
from sqlalchemy.orm import Session
from database import get_db
import models, oauth2
import schemas.group
import schemas.member
from schemas.user import TokenData
from datetime import datetime
import repository
import schemas.member



router = APIRouter(tags=['Members'], prefix="/members")

@router.post('', status_code=201)
def create_member_request(groupname: schemas.member.CreateMember, db : Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    repository.member.create_member_request(groupname.group_name, current_user.username, db)
    return {"Created"}

@router.post('/invite', status_code=201)
def invite_member_request(invitation: schemas.member.InviteMember, current_user: TokenData = Depends(oauth2.get_current_user), db : Session = Depends(get_db)):
    repository.member.invite_member_request(invitation, current_user.username, db)
    return {"Created"}

@router.get('/admins', status_code=200,  response_model=list[schemas.member.ShowMember])
def get_admin(group_name:str, db : Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return repository.member.get_admin(group_name, current_user.username, db)
    
    
@router.get('', status_code=200, response_model=list[schemas.member.ShowMember])
def get_member(group_name:str,db : Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return repository.member.get_member(group_name,current_user.username, db)