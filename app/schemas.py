from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str

class CreateUser(UserBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ContactBase(BaseModel):
    name:str
    contact:str

class CreateContact(ContactBase):
    pass

class Contact(ContactBase):
    name:str
    contact:str
    owner_id:int
    id:int
    created_at:datetime
    owner: UserOut
    class Config:
        orm_mode = True

class ContactOut(BaseModel):
    Contact:Contact
    votes:int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    contact_id: int
    dir: conint(le=1)

class VoteOut(BaseModel):
    contact_id: int
    user_id: int
    class Config:
        orm_mode=True