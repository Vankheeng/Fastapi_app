from pydantic import BaseModel
from schemas.user import User
from typing import List

class CreateGroup(BaseModel):
    name: str
    class Config():
        from_attributes = True
        
class ShowGroup(BaseModel):
    id: int
    name:str
    # Admin: List[User]
    class Config():
        from_attributes = True