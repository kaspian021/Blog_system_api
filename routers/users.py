from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from schemes import users
from Tools import dependence, auth
from database.models_database import users as database
from settings import settings

router_users = APIRouter()


@router_users.post('/Users/register_user', response_model=users.UserShowAccountInfo)
async def register_user(user_item: users.UserCreateAccount, db: Session = Depends(dependence.get_session)):
    try:
        if not user_item:
            raise HTTPException(status_code=400, detail='Error is not validation param')

        result_query = db.query(database.Users).filter(database.Users.email == user_item.email).first()

        if result_query:
            raise HTTPException(status_code=400, detail='Error email is exist already')

        result_password_create= auth.create_hash_password(user_item.password)

        user_result = database.Users(email=user_item.email, username=user_item.username, password=result_password_create)
        userShow=users.UserShowAccountInfo(email=user_item.email,username=user_item.username,password=user_item.password)
        db.add(user_result)
        db.commit()
        db.refresh(user_result)
        return userShow
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error server response')


@router_users.post('/Users/login_user', response_model=users.UserShowAccountInfoLogin)
async def login_user(user_item: users.UserBaseModel, db: Session = Depends(dependence.get_session)):
    try:


        if not user_item:
            raise HTTPException(status_code=400, detail='is not validate param')



        query = db.query(database.Users).filter(database.Users.email == user_item.email).first()
        if not query:
            raise HTTPException(status_code=404, detail='noting email in database and validate password Error')

        #decode password method and result database:
        password_result= auth.verify_password(user_item.password,query.password)

        if not password_result:
            raise HTTPException(status_code=400,detail='password Error not verify')

        token_result = auth.create_token(
            data={
                'email': query.email,
                'username': query.username,
                'role': [
                    'isSeller','user'
                ],
                'expire': settings.TOKEN_TIME_AUTHENTICATION
            }
        )

        userItem = users.UserShowAccountInfoLogin(
            id=query.id, email=query.email, username=query.username,
            password=user_item.password,token=token_result
        )


        return userItem

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error server response')
