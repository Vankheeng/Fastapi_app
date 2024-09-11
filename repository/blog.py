from fastapi import Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from oauth2 import get_current_user
import models, schemas, repository
import schemas.blog
from schemas.user import TokenData
from models import Blog, Member, User, Group, Comment, Reaction
from datetime import datetime

def create_blog(request: schemas.blog.CreateBlog, username: str,
                db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    group = db. query(Group).filter(Group.name == request.group_name).first()
    if not group:
        raise HTTPException(status_code=404, detail=f"Group {request.group_name} doesn't exist")
    member = db.query(Member).filter(Member.user_id == user.id,
                                    Member.group_id == group.id).first()
    if not member or member.role < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only members of this group can do this.")
    blog_status = 0
    if member.role == 2:
        blog_status = 1
    new_blog = Blog(
        group_id = group.id,
        user_id = user.id,
        content = request.content,
        status = blog_status,
        create_time = datetime.now()
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"Created"}

def get_blogs(group_name: str, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    group = db. query(Group).filter(Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404, detail=f"Group {group_name} doesn't exist")
    member = db.query(Member).filter(Member.user_id == user.id,Member.group_id == group.id, 
                                     Member.role >= 2).first()
    if not member :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only members of this group can do this.")
    blogs = db.query(Blog).filter(Blog.group_id == group.id, Blog.status == 1).all()
    return blogs

def get_blog_of_user(request: schemas.blog.GetBlog, username: str, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.username == username).first()
    group = db. query(Group).filter(Group.name == request.group_name).first()
    if not group:
        raise HTTPException(status_code=404, detail=f"Group {request.group_name} doesn't exist")
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {request.username} doesn't exist")
    current_member = db.query(Member).filter(Member.user_id == current_user.id,Member.group_id == group.id, 
                                     Member.role >= 2).first()
    if not current_member :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only members of this group can do this.")
        
    # member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == group.id, Member.role >= 2).first()
    # if not member:
    #     raise HTTPException(status_code=404, detail=f"User {request.username} isn't member of this group.")
    
    blogs = db.query(Blog).filter(Blog.group_id == group.id, Blog.user_id == user.id, 
                                  Blog.status == 1).all()
    return blogs
    
def get_waiting_blogs(group_name: str, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    group = db. query(Group).filter(Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404, detail=f"Group {group_name} doesn't exist")
    member = db.query(Member).filter(Member.user_id == user.id,Member.group_id == group.id, 
                                     Member.role == 2).first()
    if not member :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only admins of this group can do this task.")
    blogs = db.query(Blog).filter(Blog.group_id == group.id, Blog.status == 0).all()
    return blogs

def accept_blog(request:schemas.blog.AcceptBlog, username: str, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == request.blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog {request.blog_id} is invalid")
    group = db.query(Group).filter(Group.id == blog.group_id).first()
    admin = repository.member.is_admin(group.name, username, db)
    if request.accecpt == 0:
        db.delete(blog)
        db.commit()
    else:
        blog.status = 1
        db.commit()
    return{"Done"}

def delete_blog(blog_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog {blog_id} is invalid")
    group = db.query(Group).filter(Group.id == blog.group_id).first()
    member = db.query(Member).filter(Member.user_id == user.id,
                                     Member.group_id == group.id).first()
    if user.id == blog.user_id or (member is not None and member.role == 2):
        comments = db.query(Comment).filter(Comment.blog_id == blog_id).delete
        reactions = db.query(Reaction).filter(Reaction.blog_id == blog_id).delete
        db.delete(blog)
        return{"Deleted"}
    raise HTTPException(status_code=400, detail="You can not delete this blog")
