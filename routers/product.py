from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from Tools.dependence import get_session, get_current_user_token
from schemes import product as product
from database.models_database import product as models_database

routerProduct = APIRouter()


@routerProduct.post('/product/create_products', response_model=product.ResultModel)
async def create_product(product_item: product.ProductCreate, db: Session = Depends(get_session),
                         current_user=Depends(get_current_user_token)):
    try:
        if product_item is not None:
            exist_database = db.query(models_database.Products).filter(
                models_database.Products.image_path == product_item.image_path).first()
            if exist_database:
                raise HTTPException(status_code=400, detail='product with image_path already exist')

            product_result= models_database.Products(**product_item.model_dump())
            db.add(product_result)
            db.commit()
            db.refresh(product_result)
            product_result_show = product.ProductShow(id=product_result.id,
                                               name=product_result.name,
                                               price=product_result.price,
                                               image_path=product_result.image_path, date=product_result.date,
                                               writer=product_result.writer, desc=product_result.desc,
                                               category=product_result.category, like=product_result.like,
                                               owner_id=product_result.owner_id
                                               )
            return product.ResultModel(status_code=200, message='عملیات با موفقیت انجام شد', data=product_result_show)

    except HTTPException:
        raise
    except Exception as e:
        print(f'Error: {e}')
        HTTPException(status_code=500, detail='Error server')


@routerProduct.get('/product/product_show/{product_id}', response_model=product.ResultModel)
async def product_show_by_id(product_id: int, db: Session = Depends(get_session)):
    try:
        product_query = db.query(models_database.Products).filter(models_database.Products.id == product_id).first()
        if not product_query:
            raise HTTPException(status_code=404,detail=f'not find product by id: {product_id}')

        product_result_show = product.ProductShow(id=product_query.id,
                                                  name=product_query.name,
                                                  price=product_query.price,
                                                  image_path=product_query.image_path, date=product_query.date,
                                                  writer=product_query.writer, desc=product_query.desc,
                                                  category=product_query.category, like=product_query.like,
                                                  owner_id=product_query.owner_id
                                                  )
        return product.ResultModel(status_code=200, message='عملیات با موفقیت انجام شد', data=product_result_show)

    except HTTPException:
        raise 
    except Exception as e:
        print(f'Error: {e}')
        HTTPException(status_code=500, detail='Error server')


@routerProduct.put('/product/product_update', response_model=product.ResultModel)
async def product_update(product_item: product.ProductUpdate, product_id: int, db: Session = Depends(get_session),
                         current_user=Depends(get_current_user_token)):
    try:
        if product_id:
            query = db.query(models_database.Products).filter(models_database.Products.id == product_id).first()
            if not query:
                raise HTTPException(status_code=404, detail='ایدی که ارسال کردید وجود ندارد')

            if product_item.image_path:
                exist = db.query(models_database.Products).filter(
                    models_database.Products.image_path == product_item.image_path,
                    models_database.Products.id != product_id).first()
                if exist:
                    raise HTTPException(status_code=400, detail='image path is exist already')

            update_product = product_item.model_dump(exclude_unset=True)
            for key, value in update_product.items():
                setattr(query, key, value)
            db.commit()
            db.refresh(query)
            product_result_show = product.ProductShow(id=query.id,
                                                      name=query.name,
                                                      price=query.price,
                                                      image_path=query.image_path, date=query.date,
                                                      writer=query.writer, desc=query.desc,
                                                      category=query.category, like=query.like,
                                                      owner_id=query.owner_id
                                                      )
            return product.ResultModel(status_code=200, message='update complete is True', data=product_result_show)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error server: {e}')


@routerProduct.get('/product/show_all_product', response_model=product.ResultDataModel)
async def product_show_all(db: Session = Depends(get_session)):
    try:
        product_item = db.query(models_database.Products).all()

        if not product_item:
            return {'all_product': []}

        show_product = []
        for item in product_item:
            show_product.append(
                product.ProductShow(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    category=item.category,
                    like=item.like,
                    owner_id=item.owner_id
                )
            )

        return product.ResultDataModel(status_code=200, message='عملیات با موفقیت انجام شد',
                                       data=product.ProductAllShow(all_product=show_product))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error: {e}')


@routerProduct.get('/product/show_best_product', response_model=product.ResultDataModel)
async def product_show_best(db: Session = Depends(get_session)):
    try:
        product_item = db.query(models_database.Products).order_by(models_database.Products.like.desc()).all()

        if not product_item:
            return {'all_product': []}

        show_product = []
        for item in product_item:
            show_product.append(
                product.ProductShow(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    category=item.category,
                    like=item.like,
                    owner_id=item.owner_id
                )
            )

        return product.ResultDataModel(status_code=200, message='عملیات با موفقیت انجام شد',
                                       data=product.ProductAllShow(all_product=show_product))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error: {e}')


@routerProduct.post('/product_show_by_category', response_model=product.ResultDataModel)
async def product_show_by_category(product_category: product.ProductCategory, db: Session = Depends(get_session)):
    try:
        query = db.query(models_database.Products).filter_by(category=product_category.category).all()
        if not query:
            raise HTTPException(status_code=404, detail='is not find category in database')

        show_product = []
        for item in query:
            show_product.append(
                product.ProductShow(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    category=item.category,
                    like=item.like,
                    owner_id=item.owner_id
                )
            )

        return product.ResultDataModel(status_code=200, message='عملیات با موفقیت انجام شد',
                                       data=product.ProductAllShow(all_product=show_product))

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error is Server')


@routerProduct.get('/product_show_by/{owner_id}', response_model=product.ResultDataModel)
def product_show_by_owner_id(owner_id: int, db: Session = Depends(get_session)):
    try:
        query_result = db.query(models_database.Products).filter_by(owner_id=owner_id).all()

        if not query_result:
            raise HTTPException(status_code=404, detail='not find product')

        show_product = []
        for item in query_result:
            show_product.append(
                product.ProductShow(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    category=item.category,
                    like=item.like,
                    owner_id=item.owner_id
                )
            )

        return product.ResultDataModel(status_code=200, message='عملیات با موفقیت انجام شد',
                                       data=product.ProductAllShow(all_product=show_product))

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error server response: {e}')


@routerProduct.delete('/product_delete/{product_id}',response_model=product.ResultModel)
def product_delete_by_id(product_id:int,db:Session=Depends(get_session),token=Depends(get_current_user_token)):
    try:
        product_result= db.query(models_database.Products).filter_by(id=product_id).first()

        if not product_result:
            return product.ResultModel(status_code=404,message='ایتم مورد نظر با این مشخصات یافت نشد')

        db.delete(product_result)
        db.commit()
        db.refresh(product_result)
        return product.ResultModel(status_code=200,message='عملیات با موفقیت انجام شد')

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='Error Server response')