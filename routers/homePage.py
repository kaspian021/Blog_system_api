from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Tools.dependence import get_session
from schemes.Home import HomeModel
from schemes import product as models
from database.models_database import users, product, category
from schemes.users import UserFollowing

router = APIRouter(tags=['Home'])


@router.get('/homePage', response_model=HomeModel)
def get_homepage(user_id: int = None, db: Session = Depends(get_session)):
    try:

        product_result = db.query(product.Products).order_by(product.Products.like.desc()).all()

        if not product_result:
            raise HTTPException(status_code=400, detail='not find product best')

        show_product = []
        for item in product_result:
            show_product.append(
                models.ProductShowAll(
                    id=item.id,
                    writer=item.writer,
                    name=item.name,
                    price=item.price,
                    date=item.date,
                    image_path=item.image_path,
                    desc=item.desc,
                    categoryId=item.categoryId,
                    like=item.like,
                    owner_id=item.owner_id
                )
            )

        category_result = db.query(category.Category).all()
        show_category = []
        for item in category_result:
            show_category.append(
                models.ShowCategory(
                    id=item.id,
                    title=item.title,
                    image=item.image
                )
            )
        if user_id:
            query = db.query(users.Users).filter_by(id=user_id).first()

            if not query:
                raise HTTPException(status_code=404, detail=f'not user_id: {user_id} find to server')

            show_following = []
            for item in query.following:
                show_following_data = {
                    "location" : item.location,
                    "username" : item.username,
                    "image_path" : item.image_path,
                    "id" : item.id,
                    'products': []
                }
                if hasattr(item, 'products') and item.products:
                    show_following_data['products'] = [
                        models.ProductShowAll(
                            name=p.name,
                            price=p.price,
                            date=p.date,
                            writer=p.writer,
                            id=p.id,
                            image_path=p.image_path,
                            desc=p.desc,
                            like=p.like,
                            categoryId=p.categoryId,
                            owner_id=p.owner_id
                        )
                        for p in item.products
                    ]

                show_following.append(UserFollowing(**show_following_data))

            result_home_model = HomeModel(
                following=show_following,
                category=show_category,
                products_best=models.ProductAllShow(all_product=show_product)

            )
        else:
            result_home_model = HomeModel(
                following=None,
                category=show_category,
                products_best=models.ProductAllShow(all_product=show_product)

            )

        return result_home_model
    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error Server response')
