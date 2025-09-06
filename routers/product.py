from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from Tools.dependence import get_session, get_current_seller_token
from schemes import product as product
from database.models_database import product as models_database
from database.models_database import users ,category
from schemes.product import ShowCategory

routerProduct = APIRouter()


@routerProduct.post('/product/create_products', response_model=product.ResultModel)
async def create_product(product_item: product.ProductCreate, db: Session = Depends(get_session),
                         current_user=Depends(get_current_seller_token)):
    try:
        if product_item is not None:
            exist_database = db.query(models_database.Products).filter(
                models_database.Products.image_path == product_item.image_path).first()
            if exist_database:
                raise HTTPException(status_code=400, detail='product with image_path already exist')

            category_result = db.query(category.Category).filter_by(id= product_item.categoryId).first()

            if not category_result:
                raise HTTPException(status_code=200,detail='همچین دسته بندی نداریم لطفا یک دسته بندی مناسب انتخاب کنید')


            product_result= models_database.Products(**product_item.model_dump())
            db.add(product_result)
            db.commit()
            db.refresh(product_result)
            product_result_show = product.ProductShow(id=product_result.id,
                                               name=product_result.name,
                                               price=product_result.price,
                                               image_path=product_result.image_path, date=product_result.date,
                                               writer=product_result.writer, desc=product_result.desc,
                                               category= ShowCategory(id=category_result.id,title=category_result.title,image=category_result.image), like=product_result.like,
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

        category_result = db.query(category.Category).filter_by(id=product_query.categoryId).first()

        if not category_result:
            raise HTTPException(status_code=200, detail='معتبر نیست/همچین دسته بندی نداریم لطفا یک دسته بندی مناسب انتخاب کنید')

        product_result_show = product.ProductShow(id=product_query.id,
                                                  name=product_query.name,
                                                  price=product_query.price,
                                                  image_path=product_query.image_path, date=product_query.date,
                                                  writer=product_query.writer, desc=product_query.desc,
                                                  category= ShowCategory(id=category_result.id,title=category_result.title,image=category_result.image) , like=product_query.like,
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
                         current_user=Depends(get_current_seller_token)):
    global category_result
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

            if product_item.categoryId :
                category_result = db.query(category.Category).filter_by(id= product_item.categoryId)

                if not category_result:
                    raise HTTPException(status_code=200,detail='دسته بندی که شما انتخاب کردید وجود ندارد!!')

            db.commit()
            db.refresh(query)
            product_result_show = product.ProductShow(id=query.id,
                                                      name=query.name,
                                                      price=query.price,
                                                      image_path=query.image_path, date=query.date,
                                                      writer=query.writer, desc=query.desc,
                                                      like=query.like,
                                                      category= ShowCategory(id=category_result.id,title=category_result.title,image=category_result.image),
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
                product.ProductShowAll(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    categoryId= item.categoryId,
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
                product.ProductShowAll(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    categoryId= item.categoryId,
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
async def product_show_by_category(categoryId: int, db: Session = Depends(get_session)):
    try:
        query = db.query(models_database.Products).filter_by(categoryId=categoryId).all()
        if not query:
            raise HTTPException(status_code=404, detail='is not find category in database')

        show_product = []
        for item in query:
            show_product.append(
                product.ProductShowAll(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    categoryId= item.categoryId,
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
                product.ProductShowAll(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    categoryId= item.categoryId,
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
def product_delete_by_id(product_id:int, db:Session=Depends(get_session), current_user:users.Users =Depends(get_current_seller_token)):
    try:
        product_result= db.query(models_database.Products).filter_by(id=product_id).first()

        if not product_result:
            return product.ResultModel(status_code=404,message='ایتم مورد نظر با این مشخصات یافت نشد')

        if product_result.owner_id != current_user.id:
            return product.ResultModel(status_code=401,message='شما مالک این مقاله نیستید!!')

        db.delete(product_result)
        db.commit()
        return product.ResultModel(status_code=200,message='عملیات با موفقیت انجام شد')

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='Error Server response')

