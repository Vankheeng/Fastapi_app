from fastapi import Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from oauth2 import get_current_user
import models, schemas, repository
import schemas.reaction
from schemas.user import TokenData
from models import Blog, Member, User, Group, Reaction
from datetime import datetime

def update_reaction(request: schemas.reaction.ReactionBase,
                   username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    blog = db.query(Blog).filter(Blog.id == request.blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog {request.blog_id} doesn't exist")
    member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == blog.group_id).first()
    if not member or member.role < 2:
        raise HTTPException(status_code=400, detail="You are not a member of this group")
    reaction = db.query(Reaction).filter(Reaction.blog_id == request.blog_id, Reaction.user_id == user.id).first()
    if not reaction:
        new_reaction = Reaction(
            user_id = user.id,
            blog_id = blog.id,
            status = request.status,
            time = datetime.now()
        )
        db.add(new_reaction)
        db.commit()
        db.refresh(new_reaction)
    elif request.status != 0:
        reaction.status = request.status
        db.commit()
    else:
        db.delete(reaction)
        db.commit
    return {"Done"}


def get_reaction_of_blog(blog_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog {blog_id} doesn't exist")
    # member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == blog.group_id).first()
    # if not member or member.role < 2:
    #     raise HTTPException(status_code=400, detail="You are not a member of this group")
    return blog.reactions
    