from fastapi import Request
from src.business.file_business import FileBusiness
from src.business.vector_business import VectorBusiness
from src.business.chat_business import ChatBusiness


def file_business(request: Request) -> FileBusiness:
    return FileBusiness(mongo_db=request.app.state.mongo_db)


def vector_business(request: Request) -> VectorBusiness:
    return VectorBusiness(mongo_db=request.app.state.mongo_db)


def chat_business(request: Request) -> ChatBusiness:
    return ChatBusiness(mongo_db=request.app.state.mongo_db)
