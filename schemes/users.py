from datetime import timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, field_validator
from .product import ProductShow

class UserBaseModel(BaseModel):
    email: EmailStr



class UserCreateAccount(UserBaseModel):
    username:str
    password: str = Field(..., min_length=8, max_length=100)
    #اعتبار سنجی به صورت شخصی
    @field_validator('username',mode='before')
    @classmethod
    def check_username(cls,value):
        if not value.isalnum():
            raise ValueError('مقدار نام کاربری که وارد کرده اید باید از حروف انگلیسی و اعداد باشد')
        elif len(value) < 8 or len(value)> 20:
            raise  ValueError('مقدار نام کاربری شما باید از 8 حروف بیشتر و از 20 حروف کمتر باشد')

        return value

class UserLoginAccount(UserBaseModel):
        password: str = Field(..., min_length=8, max_length=100)

class UserShowAccountInfo(UserBaseModel):
    username:str

    class Config:
        from_attributes=True


class UserShowAccountInfoLogin(UserBaseModel):
    id:int
    username:str
    products: List[ProductShow]
    token:Optional[str]=None
    isSeller: bool
    isLogin: Optional[bool]=True





    class Config:
        from_attributes=True






