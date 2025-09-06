from sqlalchemy.orm import relationship
from database.database import Base
from sqlalchemy import Column, Integer,String


class Category (Base):
    __tablename__ = 'category'

    id = Column(Integer,primary_key=True,index=True)
    title= Column(String,nullable=False)
    image= Column(String,nullable=False)
    products = relationship('Products', back_populates='category', lazy='select')
