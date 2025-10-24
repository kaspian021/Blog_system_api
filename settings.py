
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import secrets

load_dotenv()


class Settings(BaseSettings):
    """
        این دستورات برای مقدار دهی و کنترل محرمانه token و ثبت نام است

        DATABASE_URL : ادرس دیتا بیس ما است

        SECRET_KEY: برای ساختن توکن به صورت محرمانه و رندوم به کار میرود یا همان توکنی که خروجی بهمون میده

        ALGORITHM: الگوریتمی که توکن رو برای ما encode میکند

        GOGGLE_CLIENT_ID: همان چیزی است که در گوگل کنسول میتوانیم با درست کردن پروژه جدید و اضافه کردن دسترسی ها به گوگل ایدی رسید

        GOGGLE_CLIENT_SECRET: همان چیزی است که در گوگل کنسول میتوانیم با درست کردن پروژه جدید دریافتش کنیم و بتونیم با گوگل ثبت نام انجام بدیم

        TOKEN_TIME_AUTHENTICATION: برای اینکه توکن همیشه در حالت ایمن باشه و مدت انقضا داشته باشه

        class Config: میتوان درونش با متغیر env_file بگوییم که میخوایم این تنظیمات را از چه فایلی بخونیم;



    """
    DATABASE_URL:str = os.getenv('DATABASE_URL')

    SECRET_KEY:str = os.getenv('SECRET_KEY','')


    ALGORITHM:str= os.getenv('ALGORITHM','HS256')

    GOGGLE_CLIENT_ID:str = os.getenv('GOGGLE_CLIENT_ID','')

    GOGGLE_CLIENT_SECRET:str = os.getenv('GOGGLE_CLIENT_SECRET','')

    SUPABASE_KEY:str = os.getenv('SUPABASE_KEY')
    SUPABASE_URL:str = os.getenv('SUPABASE_URL')

    #بعدا دو مورد بالا رو اضافه میکنیم

    TOKEN_TIME_AUTHENTICATION:int = int(os.getenv('TOKEN_TIME_AUTHENTICATION',30))

    print("Environment variables:")
    print("DATABASE_URL:", DATABASE_URL)
    print("SUPABASE_KEY:", SUPABASE_KEY)
    print("SUPABASE_URL:", SUPABASE_URL)
    print("SECRET_KEY:", SECRET_KEY)
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False




settings=Settings()