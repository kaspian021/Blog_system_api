from database.database import Base
from sqlalchemy import Column,Integer,String

class Users(Base):
    __tablename__= 'users'

    id= Column(Integer,primary_key=True)
    email = Column(String,unique=True)
    username= Column(String)
    password= Column(String)


