from database.database import Base
from sqlalchemy import Column, String, Integer,Date

class Products(Base):
    __tablename__ = 'products'

    id= Column(Integer,primary_key=True)
    writer= Column(String)
    name= Column(String)
    price=Column(Integer)
    date= Column(Date)
    image_path= Column(String,unique=True)
    desc=Column(String)
    category=Column(String)
    like=Column(Integer)


