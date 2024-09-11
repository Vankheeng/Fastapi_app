from pydantic import BaseModel
from schemas.user import User
from schemas.blog import ShowBlog

class ReactionBase(BaseModel):
    blog_id: int
    status: int
    
   
    
class ShowReaction(BaseModel):
    user: User
    blog: ShowBlog
    content: str
    time: str
    