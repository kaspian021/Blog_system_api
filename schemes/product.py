from datetime import date as date_type
from typing import Optional,List

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name:Optional[str]=None
    price:Optional[int]=None
    date:date_type
    writer: str



class ProductCreate(ProductBase):
    image_path: str
    desc:str
    category:str
    like:int


class ProductShow(ProductBase):
    id:int
    image_path: str
    desc:str
    category:str
    like:int
    class Confing:
        from_attributes = True

class ProductResponse(ProductBase):
    id:int

    class Confing:
        from_attributes = True



class ProductUpdate(ProductBase):
    image_path: Optional[str]=None
    desc:Optional[str]=None
    category:Optional[str]=None
    like:Optional[int]=None


class ProductAllShow(BaseModel):
    all_product: List[ProductShow]

    class Config:
        from_attributes= True


class ProductCategory(BaseModel):
    category:str




class ResultModel(BaseModel):
    status_code:int
    message: str
