from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from database import get_db
import models, schemas
from datetime import datetime
import schemas.member

def create_member_request(group_name: str, username: str, db : Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail="This group {group_name} doesn't exist")
    user = db.query(models.User).filter(models.User.username == username).first()
    member = db.query(models.Member).filter(
        models.Member.group_id == group.id, models.Member.user_id == user.id, models.Member.role >= 2).first()
    if member:
        raise HTTPException(status_code=400,
                            detail="You are already a member of this group")
    exist_request = db.query(models.Member).filter(
        models.Member.group_id == group.id, models.Member.user_id == user.id, models.Member.role == 0).first()
    # Neu da gui request (role = 0)
    if exist_request:
        raise HTTPException(status_code=400,
                            detail="You already sent request")
    new_request = models.Member(
        group_id = group.id,
        user_id = user.id,
        role = 0,
        create_time = datetime.now()
    )
    db.add(new_request)
    db.commit()
    return new_request
    
def invite_member_request(invitation: schemas.member.InviteMember, username: str, db : Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.name == invitation.group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail=f"This group {invitation.group_name} doesn't exist")
        
    user = db.query(models.User).filter(models.User.username == username).first()
    current_member = db.query(models.Member).filter(
        models.Member.group_id == group.id, models.Member.user_id == user.id).first()
    if not current_member or current_member.role < 2:
        raise HTTPException(status_code=400,
                            detail="You are not member of this group")
        
    invitee = db.query(models.User).filter(
        models.Member.group_id == group.id, models.User.username == invitation.invitee).first()
    
    if not invitee:
        raise HTTPException(status_code=404,
                            detail=f"User {invitation.invitee} doesn't exist")
    member = db.query(models.Member).filter(models.Member.user_id == invitee.id).first()
    if member is not None and member.role >= 2:
        raise HTTPException(status_code=400,
                            detail=f"User {invitation.invitee} is already a member of this group")
    if member is not None and member.role == 0:
        raise HTTPException(status_code=400,
                            detail=f"User {invitation.invitee} already sent request")
    if member is not None and member.role == 1:
        raise HTTPException(status_code=400,
                            detail=f"User {invitation.invitee} are already invited")    
    new_request = models.Member(
        group_id = group.id,
        user_id = invitee.id,
        inviter = user.id,
        role = 1,
        create_time = datetime.now()
    )
    db.add(new_request)
    db.commit()
    return new_request

def get_admin(group_name:str, username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    group = db.query(models.Group).filter(models.Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail="This group {group_name} doesn't exist")
    member = db.query(models.Member).filter(
        models.Member.group_id == group.id
        and models.Member.user_id == user.id
        ).all()
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Only members of this group can get admins")
    admins = db.query(models.Member).filter(
        models.Member.group_id == group.id, models.Member.role == 2).all()
    return admins

def get_member(group_name:str, username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    group = db.query(models.Group).filter(models.Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail="This group {group_name} doesn't exist")
    member = db.query(models.Member).filter(
        models.Member.group_id == group.id 
        and models.Member.user_id == user.id
        ).all()
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Only members of this group can get members")
    members = db.query(models.Member).filter(
        models.Member.group_id == group.id, models.Member.role >= 2).all()
    return members

def is_admin(group_name:str, username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    group = db.query(models.Group).filter(models.Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail="This group {group_name} doesn't exist")
    admin = db.query(models.Member).filter(
        models.Member.group_id == group.id, models.Member.role == 2, models.Member.user_id == user.id
        ).first()
    if admin is None:
        return False
    return True



    