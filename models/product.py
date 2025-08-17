from typing import Optional,List

from pydantic import BaseModel


class ProductBase(BaseModel):
    name:Optional[str]=None
    price:Optional[int]=None
    date:Optional[str]=None

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




class ResultModel(BaseModel):
    status_code:int
    message: str
