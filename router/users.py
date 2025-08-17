from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from models import users
from Tools import dependence
from database.models_database import users as database
router_users= APIRouter()


@router_users.post('/Users/register_user',response_model=users.UserShowAccountInfo)
async def register_user(user_item:users.UserCreateAccount,db:Session=Depends(dependence.get_session)):
    try:
        if not user_item:
            raise HTTPException(status_code=400,detail='Error is not validation param')

        result_query= db.query(database.Users).filter(database.Users.email==user_item.email).first()

        if result_query:
            raise HTTPException(status_code=400,detail='Error email is exist already')


        user_result= database.Users(email=user_item.email,username=user_item.username,password=user_item.password)

        db.add(user_result)
        db.commit()
        db.refresh(user_result)
        return user_result
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='Error server response')


@router_users.post('/Users/login_user',response_model=users.UserShowAccountInfo)
async def login_user(user_item:users.UserLoginAccount,db:Session =Depends(dependence.get_session)):
    try:
        if not user_item:
            raise HTTPException(status_code=400,detail='is not validate param')
        query=db.query(database.Users).filter(database.Users.email == user_item.email,database.Users.password==user_item.password).first()
        if not query:
            raise HTTPException(status_code=404,detail='noting email in database and validate password Error')

        db.commit()
        db.refresh(query)
        return query

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='Error server response')
