from typing import Optional, List

from pydantic import  BaseModel
from .product import ProductAllShow, ShowCategory
from .users import UserFollowing




class HomeModel(BaseModel):
    following: Optional[List[UserFollowing]]=None
    category: Optional[List[ShowCategory]]= None
    products_best: Optional[ProductAllShow]=None

    class Config:
        from_attributes= True




