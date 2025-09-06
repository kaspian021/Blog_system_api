from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from Tools.auth import remove_token, create_token, verify_token_user
from Tools.dependence import get_session,get_current_user_token
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
                                     password=result_password_create,products=[])


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

        role= ['is_login']
        if query.is_Seller:
           role.append('is_Seller')

        token_result =await auth.create_token(
            data={
                'email': query.email,
                'username': query.username,
                'role': role,
                'expire': settings.TOKEN_TIME_AUTHENTICATION
            }
        )


        show_product = []
        for item in query.products:
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

        # تبدیل followers
        followers = []
        if query.followers:
            for follow in query.followers:
                follow_data = {
                    "id": follow.id,
                    "username": follow.username,
                    "image_path": follow.image_path,
                    "products": []
                }

                # تبدیل products هر follower
                if hasattr(follow, 'products') and follow.products:
                    follow_data["products"] = [
                        product.ProductShowAll(
                            id=p.id,
                            writer=p.writer,
                            name=p.name,
                            price=p.price,
                            date=p.date,
                            image_path=p.image_path,
                            desc=p.desc,
                            categoryId= p.categoryId,
                            like=p.like,
                            owner_id=p.owner_id
                        )
                        for p in follow.products
                    ]

                followers.append(users.UserFollowers(**follow_data))

        # تبدیل following
        following = []
        if query.following:
            for follow_ing in query.following:
                follow_data_following = {
                    "id": follow_ing.id,
                    "username": follow_ing.username,
                    "location": follow_ing.location if follow_ing.location else None,
                    "image_path": follow_ing.image_path,
                    "products": []
                }

                # تبدیل products هر following
                if hasattr(follow_ing, 'products') and follow_ing.products:
                    follow_data_following["products"] = [
                        product.ProductShowAll(
                            id=p.id,
                            writer=p.writer,
                            name=p.name,
                            price=p.price,
                            date=p.date,
                            image_path=p.image_path,
                            desc=p.desc,
                            categoryId= p.categoryId,
                            like=p.like,
                            owner_id=p.owner_id
                        )
                        for p in follow_ing.products
                    ]

                following.append(users.UserFollowing(**follow_data_following))

        user_item = users.UserShowAccountInfoLogin(
            id=query.id,
            email=query.email,
            username=query.username,
            image_path=query.image_path,
            token=token_result,
            products=show_product,
            following=following,
            followers=followers,
            location=query.location
        )

        return user_item

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail='Error server response')


@router_users.post('/follow_user/{seller_id}', response_model=users.ResultBaseModel)
def follow_user(
        seller_id: int,
        current_user: database.Users = Depends(get_current_user_token),  # ✅ کاربر جاری
        db: Session = Depends(get_session)
):
    try:

        seller = db.query(database.Users).filter(database.Users.id == seller_id).first()

        if not seller:
            raise HTTPException(status_code=404, detail=f'فروشنده با آیدی {seller_id} یافت نشد')

        if not seller.is_Seller:
            raise HTTPException(status_code=400,detail='این فرد فروشنده نیست بنابراین نمیتوانید ان را فالو داشته باشید')

        if seller in current_user.following:
            raise HTTPException(status_code=400, detail='شما قبلاً این فروشنده را فالو کرده‌اید')

        if not seller.is_Seller:
            raise HTTPException(status_code=400,detail='این فرد فروشنده نیست بنابراین نمیتوانید ان را فالو داشته باشید')

        if current_user.id == seller_id:
            raise  HTTPException(status_code=400,detail='شما نمیتوانید خودتان را فالو کنید!!')



        current_user.following.append(seller)
        db.commit()

        return users.ResultBaseModel(status_code=200, message='عملیات با موفقیت انجام شد')

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail='خطای سرور')


@router_users.delete('/unfollow_user/{seller_id}',response_model=users.ResultBaseModel)
def unfollow_user(seller_id:int, db:Session=Depends(get_session), current_user:database.Users= Depends(get_current_user_token)):
    try:
        query= db.query(database.Users).filter_by(id=seller_id).first()

        if not query:
            raise HTTPException(status_code=404,detail='همچین فروشنده ای در سرور موجود نمیباشد!!')

        if query not in current_user.followers:
            raise HTTPException(status_code=404,detail='فروشنده در دنبال کننده های شما نیست!!')

        current_user.followers.remove(query)
        db.commit()

        return users.ResultBaseModel(status_code=200,message='عملیات با موفقیت انجام شد')

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='Error server response')


@router_users.post('/authentication_to_is_seller',response_model=users.UserInfoToSeller)
async def authentication_to_is_seller(user_id:int, user_info:users.UserInfoWithToIsSeller, db:Session=Depends(get_session), current_user:database.Users = Depends(get_current_user_token)):
    try:
        query_result= db.query(database.Users).filter(database.Users.id==user_id).first()

        if not query_result:
            raise HTTPException(status_code=404,detail='همچین کاربری وجود ندارد')


        token_verify= verify_token_user(user_info.token)

        if token_verify.get('email') != user_info.email:
            raise HTTPException(status_code=400,detail='ایمیلی که وارد کردید درست نیست دوباره امتحان کنید')

        var = 'is_Seller'
        result_role= token_verify.get('roles',[])

        if any(role in var for role in result_role):
            raise HTTPException(status_code=400,detail='شما از قبل هم فروشنده هستید')

        await remove_token(user_info.token)


        token_new= await create_token(data={

            'email': user_info.email,
            'company_name':user_info.company_name,
            'role': ['is_Seller','is_Login'],
            'expire': settings.TOKEN_TIME_AUTHENTICATION+2000

        })

        if not token_new:
            raise HTTPException(status_code=400,detail='توکن جدید برای شما ساخته نشد متاسفانه دوباره امتحان کنید')

        #باید بعدا با یک پکیج بتونیم با استفاده از geopoint که به دستمون میرسه ادرس فارسی رو به خروجی بدیم
        user_item = users.UserInfoToSeller(
            email=user_info.email,company_name=user_info.company_name,location=query_result.location,
            followers=query_result.followers,token=token_new,
        )
        query_result.is_Seller = True
        user_update = user_info.model_dump(exclude_unset=True)
        for key, value in user_update.items():
            setattr(query_result,key,value)


        db.commit()
        db.refresh(query_result)
        return user_item

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail='Error Server response')






