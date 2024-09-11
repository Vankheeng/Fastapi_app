import models, schemas
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, oauth2
import schemas.group
from schemas.user import TokenData
from datetime import datetime
from models import Group, Member, User, Blog, Reaction, Comment

def create_group(request: schemas.group.CreateGroup , current_user: int , db : Session = Depends(get_db)):
    group = db.query(Group).filter(Group.name == request.name).first()
    if group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This group name existed")
    new_group = Group(name = request.name)
    db.add(new_group)
    db.commit()
    new_member = Member(
        group_id = new_group.id,
        user_id = current_user,
        role = 2,
        create_time = datetime.now()
        )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_group

def find_group(groupname: str, db: Session = Depends(get_db)):
    groups = db.query(Group).filter(Group.name == groupname).first()
    if not groups:
        raise HTTPException(status_code=404, detail="This group {groupname} doesn't exist")
    return groups

def delete_group(groupname: str, db: Session = Depends(get_db),  current_user: str = Depends()):
    user = db.query(User).filter(User.username == current_user.username).first()
    group = db.query(Group).filter(Group.name == groupname).first()
    
    if not group: 
        raise HTTPException(status_code=400, 
                            detail=f"Couldn't find this group {groupname}")
        
    member = db.query(Member).filter(Member.user_id == user.id,
                                            Member.group_id == group.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not this group's member")
    if(member.role != 2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only admin can delete groups")
    
    db.delete(group)
    members = db.query(Member).filter(Member.group_id == group.id).delete
    blogs = db.query(Blog).filter(Blog.group_id == group.id).all()
    if blogs:
        for blog in blogs:
            db.query(Comment).filter(Comment.blog_id == blog.id).delete
            db.query(Reaction).filter(Reaction.blog_id == blog.id).delete
            db.delete(blog)
    db.commit()
    return{"Deleted"}
    
    