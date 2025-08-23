from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from schemes import users
from Tools import dependence, auth
from database.models_database import users as database
from settings import settings
from schemes import product
router_users = APIRouter()


@router_users.post('/Users/register_user', response_model=users.UserShowAccountInfo)
async def register_user(user_item: users.UserCreateAccount, db: Session = Depends(dependence.get_session)):
    try:
        if not user_item:
            raise HTTPException(status_code=400, detail='Error is not validation param')

        result_query = db.query(database.Users).filter(database.Users.email == user_item.email).first()

        if result_query:
            raise HTTPException(status_code=400, detail='Error email is exist already')

        result_password_create = auth.create_hash_password(user_item.password)

        user_result = database.Users(email=user_item.email, username=user_item.username,
                                     password=result_password_create, isSeller=False, isLogin=True,products=[])


        user_show = users.UserShowAccountInfo(email=user_item.email, username=user_item.username)
        db.add(user_result)
        db.commit()
        db.refresh(user_result)
        return user_show
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error server response')


@router_users.post('/Users/login_user', response_model=users.UserShowAccountInfoLogin)
async def login_user(user_item: users.UserLoginAccount, db: Session = Depends(dependence.get_session)):
    try:

        if not user_item:
            raise HTTPException(status_code=400, detail='is not validate param')

        query = db.query(database.Users).filter(database.Users.email == user_item.email).first()
        if not query:
            raise HTTPException(status_code=404, detail='noting email in database and validate password Error')

        # decode password method and result database:
        password_result = auth.verify_password(user_item.password, query.password)

        if not password_result:
            raise HTTPException(status_code=400, detail='password Error not verify')

        token_result = auth.create_token(
            data={
                'email': query.email,
                'username': query.username,
                'expire': settings.TOKEN_TIME_AUTHENTICATION
            }
        )
        show_product = []
        for item in query.products:
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


        user_item = users.UserShowAccountInfoLogin(
            id=query.id, email=query.email, username=query.username,
            token=token_result, products=show_product, isSeller=False, isLogin=True
        )

        return user_item

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error server response')
