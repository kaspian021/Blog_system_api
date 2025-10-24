import os

import uvicorn
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from database.models_database.relationship import setup_relationship
bearer_scheme = HTTPBearer(auto_error=False,scheme_name='Bearer: ',bearerFormat='Bearer',description='send token so to be can you use api')

setup_relationship()

if __name__ =='__main__':
    print("Environment variables:")
    print("DATABASE_URL:", os.getenv('DATABASE_URL'))
    print("SUPABASE_KEY:", os.getenv('SUPABASE_KEY'))
    print("SUPABASE_URL:", os.getenv('SUPABASE_URL'))
    print("SECRET_KEY:", os.getenv('SECRET_KEY'))
    uvicorn.run('config:app',port=8000,reload=True)





