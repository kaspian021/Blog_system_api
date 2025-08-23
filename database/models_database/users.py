from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column,Integer,String,Boolean

class Users(Base):
    __tablename__= 'users'

    id= Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    username= Column(String)
    password= Column(String)
    isSeller= Column(Boolean,index=True)
    isLogin= Column(Boolean)
    products= relationship('Products',back_populates='owner',lazy='select') #رابطه 1 به چند در دیتا بیس



