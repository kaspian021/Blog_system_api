from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey


class Products(Base):
    __tablename__ = 'products'

    id= Column(Integer,primary_key=True,index=True)
    writer= Column(String)
    name= Column(String)
    price=Column(Integer)
    date= Column(Date)
    image_path= Column(String,unique=True)
    desc=Column(String)
    like=Column(Integer,index=True)
    owner_id= Column(Integer,ForeignKey('users.id'),index=True)
    owner= relationship('Users',back_populates='products',lazy='select') # ارتباط بین پارامتر در table users و table products با استفاده از relationship , back_populates
    categoryId= Column(Integer,ForeignKey('category.id'),index=True)

