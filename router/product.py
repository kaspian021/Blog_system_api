from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from Tools.dependence import get_session
from models import product as product
from database.models_database import product as models_database


routerProduct= APIRouter()

@routerProduct.post('/product/create_products',response_model=product.ProductResponse)
async def create_product(product_item:product.ProductCreate,db:Session =Depends(get_session)):
    try:
        if product_item is not None:
            exist_database= db.query(models_database.Products).filter(
                models_database.Products.image_path == product_item.image_path).first()
            if exist_database:
                raise HTTPException(status_code=400,detail='product with image_path already exist')

            product= models_database.Products(**product_item.model_dump())
            db.add(product)
            db.commit()
            db.refresh(product)
            return product

    except HTTPException:
        raise
    except Exception as e:
        print(f'Error: {e}')
        HTTPException(status_code=500,detail='Error server')



@routerProduct.get('/product/product_show/{product_id}',response_model=product.ProductShow)
async def product_show(product_id:int,db:Session = Depends(get_session)):
    try:
        product_query= db.query(models_database.Products).filter(models_database.Products.id == product_id).first()
        db.add(product_query)
        db.commit()
        db.refresh(product_query)
        return product_query
    except Exception as e:
        print(f'Error: {e}')
        HTTPException(status_code=500,detail='Error server')





@routerProduct.put('/product/product_update')
async def product_update(product_item:product.ProductUpdate,product_id:int,db: Session = Depends(get_session)):
    try:
        if product_id:
            query= db.query(models_database.Products).filter(models_database.Products.id == product_id).first()
            if not query:
                raise HTTPException(status_code=404,detail='ایدی که ارسال کردید وجود ندارد')

            if product_item.image_path:
                exist= db.query(models_database.Products).filter(
                    models_database.Products.image_path == product_item.image_path,
                    models_database.Products.id != product_id).first()
                if exist:
                    raise HTTPException(status_code=400,detail='image path is exist already')

            update_product= product_item.model_dump(exclude_unset=True)
            for key,value in update_product.items():
                setattr(query,key,value)
            db.commit()
            db.refresh(query)
            return HTTPException(status_code=200,detail='update complete is True')

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Error server: {e}')


@routerProduct.get('/product/show_all_product',response_model=product.ProductAllShow)
async def product_show_all(db:Session = Depends(get_session)):
    try:
        product_item= db.query(models_database.Products).all()

        if not product_item:
            return {'all_product': []}

        return {'all_product': product_item}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=f'Error: {e}')

