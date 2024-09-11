from fastapi import Depends, status, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from oauth2 import get_current_user
import models, schemas, repository
import schemas.comment
from schemas.user import TokenData
from models import Blog, Member, User, Group, Comment
from datetime import datetime

def create_comment(request: schemas.comment.NewComment, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    blog = db.query(Blog).filter(Blog.id == request.blog_id).first()
    
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog {request.blog_id} doesn't exist")
    member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == blog.group_id).first()
    if not member or member.role < 2:
        raise HTTPException(status_code=400, detail="You are not a member of this group")
    new_comment = Comment(
        user_id = user.id,
        blog_id = blog.id,
        content = request.content,
        time = datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def update_comment(request: schemas.comment.UpdateComment,
                   username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    comment = db.query(Comment).filter(Comment.id == request.comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail=f"Comment {request.comment_id} doesn't exist")
    blog = db.query(Blog).filter(Blog.id == comment.blog_id).first()
    member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == blog.group_id).first()
    if user.id == comment.user_id or (member is not None and member.role == 2):
        comment.content = request.content
        db.commit()
        return {"Updated"}  
    else:
        raise HTTPException(status_code=400, detail="You can't delete this comment")
    

def delete_comment(comment_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail=f"Comment {comment_id} doesn't exist")
    blog = db.query(Blog).filter(Blog.id == comment.blog_id).first()
    member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == blog.group_id).first()
    if user.id == comment.user_id or (member is not None and member.role == 2):
        db.delete(comment)
        db.commit()
        return {"Deleted"}
    else:
        raise HTTPException(status_code=400, detail="You can't delete this comment")

def get_comment_of_blog(blog_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog {blog_id} doesn't exist")
    member = db.query(Member).filter(Member.user_id == user.id, Member.group_id == blog.group_id).first()
    if not member or member.role < 2:
        raise HTTPException(status_code=400, detail="You are not a member of this group")
    return blog.comments
    