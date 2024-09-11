from pydantic import BaseModel
from schemas.user import User
from schemas.group import ShowGroup

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
        
class ShowRequest(BaseModel):
    user: User
    class Config():
        from_attributes = True
    
class ShowInvitation(BaseModel):
    # groupname: ShowGroup
    inviter: User
    class Config():
        from_attributes = True
        
class Request(BaseModel):
    group_name: str

class InviteMember(BaseModel):
    group_name:str
    invitee: str
    
class ConfirmInvitation(BaseModel):
    group_name: str
    accept: int
    
    
class RoleUpdate(BaseModel):
    group_name: str
    username: str
    new_role: int
    