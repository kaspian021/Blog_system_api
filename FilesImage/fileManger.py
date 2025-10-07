from supabase.client import create_client,Client
from settings import settings
from fastapi import HTTPException, UploadFile,File


async def upload_image(supabase_bucket:str,file_path:str,content,file:UploadFile=File()):
    try:
        if not content:
            raise HTTPException(status_code=400,detail='content file not invalidate')

        supabase_login: Client = create_client(supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY)
        upload_supabase = supabase_login.storage.from_(supabase_bucket).upload(
            file_path,
            content,
            {"content-type": file.content_type}
        )

        if hasattr(upload_supabase, 'error') and upload_supabase.error:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {upload_supabase.error.message}")

        image_url = supabase_login.storage.from_(supabase_bucket).get_public_url(file_path)

        if not image_url:
            raise HTTPException(status_code=500,detail='Error Server Image not upload')

        return image_url
    except Exception as e:
        print(f'Error:{e}')
        raise HTTPException(status_code=500,detail=f'Error Server {e}')