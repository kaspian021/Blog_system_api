from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserBaseModel(BaseModel):
    email: EmailStr
    password:str = Field(...,min_length=8,max_length=20)


class UserCreateAccount(UserBaseModel):
    username:str


class UserLoginAccount(UserBaseModel):
    token: Optional[str]=None



class UserShowAccountInfo(UserBaseModel):
    id:int
    username:str
    token:Optional[str]=None

    class Config:
        from_attributes=True

