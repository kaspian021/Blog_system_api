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




def get_current_user_token( db: Session = Depends(get_session),
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
        email = verify_token_user(token)

        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials!!')


        if email is None:
            raise HTTPException(status_code=400, detail='not is validation in data bad valid')

        query_result = db.query(database.Users).filter_by(email=email).first()

        if not query_result:
            raise HTTPException(status_code=404, detail='email nothing in database')

        return query_result





    except HTTPException:
        raise


    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error server response: {e}')

