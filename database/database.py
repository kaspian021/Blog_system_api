
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SqlAlchemy_Database_Url= 'sqlite:///./sql_app.db'

engine= create_engine(SqlAlchemy_Database_Url,connect_args={'check_same_thread':False})

sessionLocale= sessionmaker(bind=engine)
Base= declarative_base()