from typing import Annotated
from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str
    
    
class User(UserBase):
    name: str 
    class Config:
        from_attribute = True
        
        
class CreateUser(UserBase):
    name: str
    password: str
    class Config:
        from_attribute = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # id: int
    username: str

    class Config:
        from_attribute = True    
        
class UpdateUser(BaseModel):
    name: str
    password:str
    class Config:
        from_attribute = True    