from fastapi import APIRouter
from src.endpoint.file_endpoint import file_router
from src.endpoint.vector_endpoint import vector_router

main_router = APIRouter()

main_router.include_router(file_router, prefix="/coder-buddy")
main_router.include_router(vector_router, prefix="/coder-buddy")
