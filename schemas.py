from datetime import datetime
from pydantic import BaseModel

    
class PostBase(BaseModel):
    title: str
    content: str
    
class UserBase(BaseModel):
    username: str
    email: str

class UserLogin(BaseModel):
    username:str
    password: str

class PostCreate(PostBase):
    pass

class User(UserBase):
    id: int

class UserCreate(UserBase):
    password: str
        
class showUser(BaseModel):
    username:str
    id: int
    
    class Config:
        orm_mode = True
        
class Post(PostBase):
    id: str
    author: showUser
    
    class Config:
        orm_mode = True