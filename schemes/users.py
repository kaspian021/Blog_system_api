from datetime import timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, field_validator


class UserBaseModel(BaseModel):
    email: EmailStr
    password:str = Field(...,min_length=8,max_length=100)


class UserCreateAccount(UserBaseModel):
    username:str
    #اعتبار سنجی به صورت شخصی
    @field_validator('username',mode='before')
    @classmethod
    def check_username(cls,value):
        if not value.isalnum():
            raise ValueError('مقدار نام کاربری که وارد کرده اید باید از حروف انگلیسی و اعداد باشد')
        elif len(value) < 8 or len(value)> 20:
            raise  ValueError('مقدار نام کاربری شما باید از 10 حروف بیشتر و از 20 حروف کمتر باشد')

        return value





class UserShowAccountInfo(UserBaseModel):
    username:str


class UserShowAccountInfoLogin(UserBaseModel):
    id:int
    username:str
    token:Optional[str]=None





    class Config:
        from_attributes=True






