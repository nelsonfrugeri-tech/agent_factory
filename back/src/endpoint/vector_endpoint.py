from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any
from src.business.vector_business import VectorBusiness

class CreateKnowledgeBaseRequest(BaseModel):
    name: str

class AddFilesRequest(BaseModel):
    file_ids: List[str]

vector_router = APIRouter()
vector = VectorBusiness()

@vector_router.post(
    "/v1/vectors",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}}
)
async def create_knowledge_base(request: CreateKnowledgeBaseRequest) -> str:
    try:
        knowledge_base_id = vector.create_knowledge_base(request.name)
        return knowledge_base_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@vector_router.post(
    "/v1/vectors/{vector_id}/files",
    response_model=List[str],
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}}
)
async def add_files(vector_id: str, request: AddFilesRequest) -> List[str]:
    try:
        vector.add_files(vector_id, request.file_ids)
        return request.file_ids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@vector_router.get(
    "/v1/vectors/{vector_id}/files",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}}
)
async def get_vector_files(vector_id: str) -> Dict[str, Any]:
    try:
        result = vector.get_vector_files(vector_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
