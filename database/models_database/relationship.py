from .category import Category
from .product import Products
from sqlalchemy.orm import  relationship



def setup_relationship():
    Category.products = relationship('Products', back_populates='category', lazy='select')
    Products.category = relationship('Category', back_populates='products', lazy='select')



