from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from database import get_db
import models, schemas
from datetime import datetime
import schemas.member
from models import Group, Member, User, Comment, Reaction, Blog



def get_admin(group_name:str, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail="This group {group_name} doesn't exist")
    member = db.query(Member).filter(
        Member.group_id == group.id, Member.user_id == user.id,
        Member.role >= 2).all()
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Only members of this group can get admins")
    admins = db.query(Member).filter(
        Member.group_id == group.id, Member.role == 2).all()
    return admins

def get_members(group_name:str, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail= f"This group {group_name} doesn't exist")
    member = db.query(Member).filter(
        Member.group_id == group.id, Member.user_id == user.id,
        Member.role >= 2
        ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Only members of this group can get members")
    members = db.query(Member).filter(
        Member.group_id == group.id, Member.role >= 2).all()
    return members

def is_admin(group_name:str, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail= f"This group {group_name} doesn't exist")
    admin = db.query(Member).filter(
        Member.group_id == group.id, Member.role == 2, Member.user_id == user.id
        ).first()
    if not admin:
        raise HTTPException(status_code=404,
                            detail="Only admin can do it.")
    return admin

def get_all_requests(groupname: str, username: str, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.name == groupname).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail= f"This group {groupname} doesn't exist")
    user = db.query(User).filter(User.username == username).first()
    admin = is_admin(groupname, username, db)
    member = db.query(Member).filter(Member.group_id == group.id, Member.role == 0).all()
    return member

def get_all_invitations(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    invitations = db.query(Member).filter(Member.user_id == user.id,
                                                 Member.role == 1).all()
    return invitations


def create_member_request(group_name: str, username: str, db : Session = Depends(get_db)):
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail= f"Group {group_name} doesn't exist")
    user = db.query(User).filter(User.username == username).first()
    member = db.query(Member).filter(
        Member.group_id == group.id, Member.user_id == user.id).first()
    if member:
        if member.role >= 2:
            raise HTTPException(status_code=400,
                            detail="You are already a member of this group")
        if member.role == 0:
            raise HTTPException(status_code=400,
                                detail="You already sent request")
        if member.role == 1:
            member.role = 0
            db.commit()
            raise HTTPException(status_code=200)
    new_request = Member(
        group_id = group.id,
        user_id = user.id,
        role = 0,
        create_time = datetime.now()
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request
    
def invite_member(invitation: schemas.member.InviteMember, username: str, db : Session = Depends(get_db)):
    group = db.query(Group).filter(Group.name == invitation.group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail=f"This group {invitation.group_name} doesn't exist")
        
    user = db.query(User).filter(User.username == username).first()
    current_member = db.query(Member).filter(
        Member.group_id == group.id, Member.user_id == user.id).first()
    if not current_member or current_member.role < 2:
        raise HTTPException(status_code=400,
                            detail="You are not member of this group")
        
    invitee = db.query(User).filter(User.username == invitation.invitee).first()
    
    if not invitee:
        raise HTTPException(status_code=404,
                            detail=f"User {invitation.invitee} doesn't exist")
    member = db.query(Member).filter(Member.user_id == invitee.id,
                                            Member.group_id == group.id).first()
    if member is not None and member.role >= 2:
        raise HTTPException(status_code=400,
                            detail=f"User {invitation.invitee} is already a member of this group")
    if member is not None and member.role == 0:
        raise HTTPException(status_code=400,
                            detail=f"User {invitation.invitee} already sent request")
    if member is not None and member.role == 1:
        raise HTTPException(status_code=400,
                            detail=f"User {invitation.invitee} are already invited")    
    new_request = Member(
        group_id = group.id,
        user_id = invitee.id,
        inviter = user.id,
        role = 1,
        create_time = datetime.now()
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

def confirm_invitation(request: schemas.member.ConfirmInvitation, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    group = db.query(Group).filter(Group.name == request.group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail=f"This group {request.group_name} doesn't exist")
    invitation = db.query(Member).filter(Member.user_id == user.id,
                                                 Member.group_id == group.id,
                                                 ).first()
    if not invitation:
        raise HTTPException(status_code=404,
                            detail=f"You have no invitation to join group {request.group_name}")
    if invitation.role == 0:
        raise HTTPException(status_code=400,
                            detail="You sent request")
    if invitation.role >= 2:
        raise HTTPException(status_code=400,
                            detail=f"You are member of group {request.group_name}")
    else:
        if request.accept == 0:
            db.delete(invitation)
            db.commit()
        else:
            admin = db.query(Member).filter(Member.user_id == invitation.inviter,
                                                   Member.group_id == group.id).first()
            if admin and admin.role == 2:
                invitation.role = 3
            else:
                invitation.role = 0
            db.commit()
    return{"Done"}
        
    
def confirm_request(data: schemas.member.RoleUpdate, username: str, db: Session = Depends(get_db)):
    admin = is_admin(data.group_name, username, db)
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail=f"This user {data.username} doesn't exist")
    group = db.query(Group).filter(Group.name == data.group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail=f"This group {data.group_name} doesn't exist")
    request = db.query(Member).filter(Member.user_id == user.id,
                                                 Member.group_id == group.id,
                                                 ).first()
    if not request or request.role == 1:
        raise HTTPException(status_code=404,
                            detail=f"User {data.username} didn't send request to this group")
    if request.role >= 2:
        raise HTTPException(status_code=400,
                            detail=f"User {data.username} are member of group {data.group_name}")
    else:
        if data.new_role == 0:
            db.delete(request)
            db.commit()
        else:
            request.role = data.new_role
            db.commit()
            
    return {"Done"}

def role_update(data: schemas.member.RoleUpdate, username: str, db: Session = Depends(get_db)):
    admin = is_admin(data.group_name, username, db)
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404,
                            detail=f"This user {data.username} doesn't exist")
    group = db.query(Group).filter(Group.name == data.group_name).first()
    if not group:
        raise HTTPException(status_code=404,
                            detail=f"This group {data.group_name} doesn't exist")
    member = db.query(Member).filter(Member.user_id == user.id,
                                                 Member.group_id == group.id,
                                                 ).first()
    if not member or member.role <= 1:
        raise HTTPException(status_code=404,
                            detail=f"User {data.username} isn't not a member of this group")
    else:
        if data.new_role == 0:
            blogs = db.query(Blog).filter(Blog.user_id == user.id, Blog.group_id == group.id)
            for blog in blogs.all():
                db.query(Comment).filter(Comment.blog_id == blog.id).delete
                db.query(Reaction).filter(Reaction.blog_id == blog.id).delete
            blogs.delete
            db.delete(member)
            db.commit()
        else:
            member.role = data.new_role
            db.commit()
            
    return {"Done"}