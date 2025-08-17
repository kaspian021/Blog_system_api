from sqlalchemy.orm import Session

from database.database import sessionLocale

def get_session()-> Session:
    db=sessionLocale()
    try:
        yield db
    finally:
        db.close()