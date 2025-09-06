from fastapi import FastAPI
from routers import product,users,homePage,privetAdmin



app = FastAPI()
app.include_router(users.router_users,tags=['Users'])
app.include_router(product.routerProduct,tags=['Product'])
app.include_router(homePage.router,tags=['Home'])
app.include_router(privetAdmin.routerApi,tags=['Admin'])