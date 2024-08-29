import models, schemas
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, oauth2
import schemas.group
from schemas.user import TokenData
from datetime import datetime

def create_group(request: schemas.group.CreateGroup , current_user: int , db : Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.name == request.name).first()
    if group:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This group name existed")
    new_group = models.Group(name = request.name)
    db.add(new_group)
    db.commit()
    new_member = models.Member(
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
    groups = db.query(models.Group).filter(models.Group.name == groupname).first()
    if not groups:
        raise HTTPException(status_code=404, detail="This group {groupname} doesn't exist")
    return groups

def delete_group(groupname: str, db: Session = Depends(get_db),  current_user: str = Depends()):
    user = db.query(models.User).filter(models.User.username == current_user.username).first()
    group = db.query(models.Group).filter(models.Group.name == groupname).first()
    member = db.query(models.Member).filter(models.Member.user_id == user.id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not this group's member")
    if(member.role != 2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only admin can delete groups")
    if not group: 
        raise HTTPException(status_code=400, 
                            detail="Couldn't find this group {groupname}")
    db.delete(group)
    members = db.query(models.Member).filter(models.Member.group_id == group.id)
    if members is not None:
        members.delete(synchronize_session=False)
    db.commit()
    
    