
import uvicorn
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from database.models_database.relationship import setup_relationship
bearer_scheme = HTTPBearer(auto_error=False,scheme_name='Bearer: ',bearerFormat='Bearer',description='send token so to be can you use api')

setup_relationship()

if __name__ =='__main__':
    uvicorn.run('config:app',port=8000,reload=True)





