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
from typing import List
from models import Group, Member, User




router = APIRouter(tags=['Members'], prefix="/members")


@router.get('/admins', status_code=200,  response_model=List[schemas.member.ShowMember])
def get_admin(group_name:str, db : Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return repository.member.get_admin(group_name, current_user.username, db)
    
    
@router.get('', status_code=200, response_model=List[schemas.member.ShowMember])
def get_members(group_name:str,db : Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    return repository.member.get_members(group_name,current_user.username, db)

@router.get("/all_request", status_code=200, response_model=List[schemas.member.ShowRequest])
def get_all_requests(groupname, current_user: TokenData = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return repository.member.get_all_requests(groupname, current_user.username, db)

@router.get("/all_invitations", status_code=200,
            # response_model=List[schemas.member.ShowInvitation]
            )
def get_all_invitations(current_user: TokenData = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return repository.member.get_all_invitations(current_user.username, db)


@router.post('', status_code=201)
def create_member_request(groupname: schemas.member.CreateMember, 
                          db : Session = Depends(get_db), current_user: TokenData = Depends(oauth2.get_current_user)):
    repository.member.create_member_request(groupname.group_name, current_user.username, db)
    return {"Created"}

@router.post('/invite', status_code=201)
def invite_member(invitation: schemas.member.InviteMember, 
                          current_user: TokenData = Depends(oauth2.get_current_user), db : Session = Depends(get_db)):
    repository.member.invite_member(invitation, current_user.username, db)
    return {"Created"}

@router.put("/confirm_invitations", status_code=200)
def confirm_invitation(request: schemas.member.ConfirmInvitation, 
                       current_user: TokenData = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):  
    return repository.member.confirm_invitation(request, current_user.username, db)

@router.put("/confirm_request", status_code=200)
def confirm_request(data: schemas.member.RoleUpdate, current_user: TokenData = Depends(oauth2.get_current_user), 
                    db: Session = Depends(get_db)):
    return repository.member.confirm_request(data, current_user.username, db)

@router.put("/role_update", status_code=200)
def role_update(data: schemas.member.RoleUpdate, current_user: TokenData = Depends(oauth2.get_current_user), 
                db: Session = Depends(get_db)):
    return repository.member.role_update(data, current_user.username, db)