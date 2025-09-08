import re
from datetime import timedelta
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, field_validator, validator
from .product import ProductShow, ProductShowAll


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


class GeoPoint(BaseModel):
    lat:float
    long:float

    class Config:
        from_attributes=True


class UserFollowing(BaseModel):
    id:int
    username:str
    location: Optional[str] = None
    image_path:Optional[str]=None
    products: Optional[List[ProductShowAll]]=None

    class Config:
        from_attributes=True

class UserFollowers(BaseModel):
    id:int
    username:str
    image_path:Optional[str]=None
    products: Optional[List[ProductShow]]=None
    class Config:
        from_attributes=True



class UserShowAccountInfoLogin(UserBaseModel):
    id:int
    username:str
    image_path: Optional[str]=''
    products: Optional[List[ProductShowAll]]=None
    location: Optional[str] = ''
    following: Optional[List[UserFollowing]]=None
    followers: Optional[List[UserFollowers]]=None
    is_Seller: Optional[bool]=False
    token:str


    class Config:
        from_attributes=True



class UserInfoWithToIsSeller(UserBaseModel):
    company_name: str
    phone_number: str
    image_path: str
    location: str
    token: str
    is_Seller: bool

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        pattern = re.compile(r"^(\+98|0|98)?9\d{9}$")
        if not pattern.match(v):
            raise ValueError("شماره تلفن معتبر نیست")

        # تبدیل به فرمت استاندارد
        cleaned = re.sub(r'[\s\-]', '', v)
        if cleaned.startswith('0'):
            cleaned = '+98' + cleaned[1:]
        elif cleaned.startswith('98'):
            cleaned = '+' + cleaned
        elif not cleaned.startswith('+98'):
            cleaned = '+98' + cleaned[2:] if cleaned.startswith('98') else '+98' + cleaned

        return cleaned


class UserInfoToSeller(UserBaseModel):
    company_name:str
    location: Optional[GeoPoint] = None
    followers: Optional[List[UserFollowing]]=None
    token:str


    class Config:
        from_attributes=True




class ResultBaseModel(BaseModel):
    status_code:int
    message: str


