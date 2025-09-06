from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from Tools.auth import verify_token_user
from database.models_database import users as database
import main
from database.database import sessionLocale

def get_session()-> Session:
    db=sessionLocale()
    try:
        yield db
    finally:
        db.close()




def get_current_seller_token(db: Session = Depends(get_session),
                             credentials: HTTPAuthorizationCredentials = Depends(main.bearer_scheme)):



    """
    authentication swagger in validate and return result -> Token model
    :param token:
    :param db: database.session can you query.(Users database) // Depends(get_session to Tools.dependence)
    :return: information jwt
    """

    try:
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='not validate content_type: Authentication')
        token=credentials.credentials
        result_map = verify_token_user(token)

        if not result_map:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials!!')

        var = 'is_Seller'

        user_roles = result_map.get('roles',[])
        print(user_roles)

        if not any(role in var for role in user_roles):
            raise HTTPException(status_code=400, detail=f'شما رول مورد نظر را برای دسترسی به این بخش ندارید!! ')

        query_result = db.query(database.Users).filter_by(email=result_map.get('email')).first()



        if not query_result:
            raise HTTPException(status_code=404, detail='email nothing in database')



        return query_result





    except HTTPException:
        raise


    except Exception as e:
        print(f'warning: {e}')
        raise HTTPException(status_code=500, detail=f'Error server response: {e}')

def get_current_user_token(db: Session = Depends(get_session),
                           credentials: HTTPAuthorizationCredentials = Depends(main.bearer_scheme)):



    """
    authentication swagger in validate and return result -> Token model
    :param token:
    :param db: database.session can you query.(Users database) // Depends(get_session to Tools.dependence)
    :return: information jwt
    """

    try:
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='not validate content_type: Authentication')
        token=credentials.credentials
        result_map = verify_token_user(token)

        if not result_map:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials!!')

        print(result_map)
        var = 'is_login'

        user_roles = result_map.get('roles',[])

        if not any(role in var for role in user_roles):
            raise HTTPException(status_code=400, detail=f'شما رول مورد نظر را برای دسترسی به این بخش ندارید {var}')

        query_result = db.query(database.Users).filter_by(email=result_map.get('email')).first()



        if not query_result:
            raise HTTPException(status_code=404, detail='email nothing in database')



        return query_result





    except HTTPException:
        raise


    except Exception as e:
        print(f'warning: {e}')
        raise HTTPException(status_code=500, detail=f'Error server response: {e}')




def get_current_admin_token(db: Session = Depends(get_session),
                           credentials: HTTPAuthorizationCredentials = Depends(main.bearer_scheme)):



    """
    authentication swagger in validate and return result -> Token model
    :param token:
    :param db: database.session can you query.(Users database) // Depends(get_session to Tools.dependence)
    :return: information jwt
    """

    try:
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='not validate content_type: Authentication')
        token=credentials.credentials
        result_map = verify_token_user(token)

        if not result_map:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials!!')

        var = 'is_admin'

        user_roles = result_map.get('roles',[])

        if not any(role in var for role in user_roles):
            raise HTTPException(status_code=400, detail=f'شما رول مورد نظر را برای دسترسی به این بخش ندارید {var}')

        query_result = db.query(database.Users).filter_by(email=result_map.get('email')).first()



        if not query_result:
            raise HTTPException(status_code=404, detail='email nothing in database')



        return query_result





    except HTTPException:
        raise


    except Exception as e:
        print(f'warning: {e}')
        raise HTTPException(status_code=500, detail=f'Error server response: {e}')
