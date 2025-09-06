from sqlalchemy.orm import relationship

from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey

followers= Table(
    'followers',Base.metadata,
    Column('following_id', Integer,ForeignKey('users.id'),primary_key=True,index=True),
    Column('followers_id',Integer,ForeignKey('users.id'),primary_key=True,index=True)
)

class Users(Base):
    __tablename__= 'users'

    id= Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    username= Column(String)
    #چهار تا پارامتر پایین به دلیل اینکه برای کاربران عادی ضروری نیست قابلیت خالی بودن میدیم
    company_name= Column(String,nullable=True)
    phoneNumber = Column(String,nullable=True)
    image_path= Column(String,nullable=True,)
    location = Column(String,nullable=True)
    password= Column(String)
    products= relationship('Products',back_populates='owner',lazy='select') #رابطه 1 به چند در دیتا بیس
    is_Seller = Column(Boolean,nullable=True)
    # رابطه چند به چند در دیتا بیس
    following=relationship(
        'Users',secondary=followers,primaryjoin= id==followers.c.following_id,secondaryjoin= id==followers.c.followers_id,
        backref='followers',
        lazy='select'
    )



