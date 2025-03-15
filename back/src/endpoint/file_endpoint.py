from io import BytesIO
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends, Form
from pydantic import BaseModel
from typing import List, Dict, Any
from src.business.file_business import FileBusiness
from src.port.port import file_business

file_router = APIRouter()


class CreateFileRequest(BaseModel):
    project_name: str


class ProjectResponse(BaseModel):
    id: str
    name: str
    files: List[str]


@file_router.post(
    "/v1/files",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}},
)
async def create_file(
    project_name: str = Form(...),
    file: UploadFile = File(...),
    file_business: FileBusiness = Depends(file_business),
) -> ProjectResponse:
    print(f"📂 Received file: {file.filename}")
    print(f"📂 Project name: {project_name}")

    # ⚡ Lê o arquivo ANTES de validar o Content-Type
    zip_content = BytesIO(await file.read())
    file_size = zip_content.getbuffer().nbytes

    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    print(f"📏 File size: {file_size} bytes")

    try:
        project = await file_business.create_project(zip_content, project_name)
        return ProjectResponse(
            id=project.id, name=project.name, files=[file.id for file in project.files]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
