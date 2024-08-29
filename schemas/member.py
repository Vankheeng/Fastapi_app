from pydantic import BaseModel
from schemas.user import User

class CreateMember(BaseModel):
    group_name: str
        
        
class Admin(BaseModel):
    username: str
    role : str
    
class ShowMember(BaseModel):
    user: User
    role: int
    class Config():
        from_attributes = True
        
class Request(BaseModel):
    group_name: str

class InviteMember(BaseModel):
    group_name:str
    invitee: str