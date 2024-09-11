from pydantic import BaseModel
from schemas.user import User
from schemas.blog import ShowBlog

class NewComment(BaseModel):
    blog_id: int
    content: str
    
class UpdateComment(BaseModel):
    comment_id: int
    content: str

    
    
class ShowComment(BaseModel):
    user: User
    blog: ShowBlog
    content: str
    time: str
    