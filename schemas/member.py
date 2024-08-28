from pydantic import BaseModel
from schemas.user import User

class CreateMember(BaseModel):
    group_name: str
        
        
class Admin(BaseModel):
    username: str
    role : str