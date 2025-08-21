from fastapi import FastAPI
from routers import product,users



app = FastAPI()
app.include_router(users.router_users,tags=['Users'])
app.include_router(product.routerProduct,tags=['Product'])
