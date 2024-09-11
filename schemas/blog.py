from pydantic import BaseModel

class CreateBlog(BaseModel):    
    group_name: str
    content: str
    
class GetBlog(BaseModel):
    group_name: str
    username: str

class ShowBlog(BaseModel):
    username: str
    content: str
    
class AcceptBlog(BaseModel):
    blog_id: int
    accecpt: int
