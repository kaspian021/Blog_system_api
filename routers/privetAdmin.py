
from fastapi import APIRouter,Depends,HTTPException
from Tools.dependence import get_current_admin_token,get_session
from sqlalchemy.orm import Session
from schemes.users import ResultBaseModel
from schemes.product import CateGoryCreate
from database.models_database import category
routerApi = APIRouter(tags=['Admin'])


@routerApi.post('/category_post',response_model=ResultBaseModel)
def category_post(data:CateGoryCreate, db:Session = Depends(get_session),current_user = Depends(get_current_admin_token)):
    try:

        query=db.query(category.Category).filter(category.Category.title==data.title).first()

        if query:
            raise HTTPException(status_code=400,detail='شما یک ایتم به این اسم قبلا درست کردید لطفا اسم دیگه ای انتخاب کنید!!')

        query_image = db.query(category.Category).filter(category.Category.image==data.image).first()

        if query_image:
            raise HTTPException(status_code=400,detail='شما قبلا همچین تصویری در دیتا بیس ذخیره کردید لطفا یک تصویر دیگه بارگزاری کنید!!')

        result_db = category.Category(
            title=data.title,
            image=data.image
        )

        db.add(result_db)
        db.commit()

        return ResultBaseModel(status_code=200,message='عملیات با موفقیت انجام شد')

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='خطای سرور!!')

