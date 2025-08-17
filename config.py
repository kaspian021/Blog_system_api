from fastapi import FastAPI
from router import product,users

app = FastAPI()

app.include_router(product.routerProduct,tags=['Product'])
app.include_router(users.router_users,tags=['Users'])