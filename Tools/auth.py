import datetime
from types import NoneType
from typing import Optional
from datetime import timedelta
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from settings import settings




pws_context = CryptContext(schemes=['sha256_crypt'], deprecated='auto')


def create_hash_password(password: str):
    """
    create password hash with passlib.context and bcrypt
    :param password: str create account Api fastapi

    :return: password hash return
    """

    return pws_context.hash(password)


def verify_password(password_current, password_hash: str):
    """
    verify password and login Api fastapi
    :param password_hash:
    :return:
    """

    return pws_context.verify(password_current, password_hash)


def create_token(data: dict, expire: Optional[timedelta] = None) -> str:
    """
    create token in api create_account api Users

    :param data: is data dict for save information User {
    email: gmail.com
    username: alikaspian
    expire: 100 min
    }
    :param expire: time expire token
    :return: string param {token}
    """

    try:

        data_jwt = data.copy()
        current_time = datetime.datetime.utcnow()
        if expire:
            exp = int((current_time + expire).timestamp())
        else:
            exp = int((current_time + timedelta(minutes=settings.TOKEN_TIME_AUTHENTICATION)).timestamp())

        data_jwt.update(
            {
                'expire': exp
            }
        )

        jwt_token = jwt.encode(claims=data_jwt, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return jwt_token
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=402, detail='token Error')

    except Exception as e:
        print(e)


def verify_token_user(token: str):
    """
    token is validate model response -> TokenModel has Token
    :param token: str
    :return: if jwt has token return: -> TokenModel{dict} else return -> Error
    """
    try:

        jwt_result = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        if not jwt_result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='توکنی پیدا نشد لطفا دوباره لاگین کنید')

        result_email = jwt_result.get('email')

        return result_email

    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Error {e}')

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error Server response')

