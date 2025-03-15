from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from typing import List
from io import BytesIO
from src.business.file_business import FileBusiness
from src.port.port import file_business

file_router = APIRouter()


@file_router.post(
    "/v1/files",
    response_model=List[str],
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
)
async def create_file(
    file: UploadFile = File(...), file_business: FileBusiness = Depends(file_business)
) -> List[str]:
    print(f"📂 Received file: {file.filename}")

    # ⚡ Lê o arquivo ANTES de validar o Content-Type
    zip_content = BytesIO(await file.read())
    file_size = zip_content.getbuffer().nbytes

    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    print(f"📏 File size: {file_size} bytes")

    try:
        file_ids = await file_business.create_file(zip_content)
        return file_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
