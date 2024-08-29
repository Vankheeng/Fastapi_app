from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    name = Column(String(200))
    hashed_password = Column(String(200))
    create_time = Column(DateTime)
    
    members = relationship("Member", back_populates = "user")
    blogs = relationship("Blog", back_populates="user")
    reactions = relationship("Reactions", back_populates="user")
    comments = relationship("Comments", back_populates="user")
    
class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    
    members = relationship("Member", back_populates="group")
    blogs = relationship("Blog", back_populates="group")
    
class Member(Base):
    __tablename__ = "members"
    
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    user_id = Column(Integer, ForeignKey("users.id"))
    inviter = Column(Integer)
    role = Column(Integer)
    create_time = Column(DateTime)
    
    user = relationship("User", back_populates="members")
    group = relationship("Group", back_populates="members")
    
class Blog(Base):
    __tablename__= "blogs"
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String(1000), nullable=False)
    Status = Column(String(100))
    
    
    user = relationship("User", back_populates="blogs")
    group = relationship("Group", back_populates="blogs")
    reactions = relationship("Reactions", back_populates="blog")
    comments = relationship("Comments", back_populates="blog")
    
class Reactions(Base):
        
    __tablename__="reactions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    status = Column(Integer, default=0)
    time = Column(DateTime)
    
    user = relationship("User", back_populates="reactions")
    blog = relationship("Blog", back_populates="reactions")
    
class Comments(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    status = Column(String(1000), nullable=False)
    time = Column(DateTime)
    
    user = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    
