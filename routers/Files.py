import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import uuid
from sqlalchemy.orm import Session
from Tools.dependence import get_session,get_current_seller_token

router_file = APIRouter(tags=['Files'])

@router_file.get('/images/{file_name}')
async def show_image(file_name:str):
    try:
        file_path = os.path.join('FilesImage',file_name)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404,detail='image not find')

        extension = file_name.split('.')[-1].lower()

        media_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'svg': 'image/svg+xml'
        }

        media_type = media_types.get(extension,'application/octet-stream')

        return FileResponse(
            status_code=200,
            path=file_path,
            filename=file_name,
            media_type=media_type
        )
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=f'Error Server {e}')




