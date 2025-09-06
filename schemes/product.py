from datetime import date as date_type
from typing import Optional,List

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name:Optional[str]='Blog_system'
    price:Optional[int]=0
    date:date_type
    writer: str

class CateGoryCreate(BaseModel):
    title: str
    image: str

    class Config:
        from_attributes= True

class ShowCategory(BaseModel):
    id: int
    title: str
    image: str

    class Config:
        from_attributes= True



class ListCategory(BaseModel):
    allCategory: Optional[List[ShowCategory]]= None


    class Config:
        from_attributes=True


class ProductCreate(ProductBase):
    image_path: str
    desc:str
    like:int
    categoryId:int
    owner_id: int


class ProductShow(ProductBase):
    id:int
    image_path: str
    desc:str
    like:int
    category: ShowCategory
    owner_id: int

    class Confing:
        from_attributes = True

class ProductShowAll(ProductBase):
    id:int
    image_path: str
    desc:str
    like:int
    categoryId: int
    owner_id: int

    class Confing:
        from_attributes = True




class ProductUpdate(ProductBase):
    image_path: Optional[str]=None
    desc:Optional[str]=None
    categoryId:Optional[int]=None
    like:Optional[int]=None


class ProductAllShow(BaseModel):
    all_product: List[ProductShowAll]

    class Config:
        from_attributes= True






class ResultBaseModel(BaseModel):
    status_code:int
    message: str


class ResultModel(ResultBaseModel):

    data: Optional[ProductShow]=None

class ResultDataModel(ResultBaseModel):

    data: Optional[ProductAllShow]=None