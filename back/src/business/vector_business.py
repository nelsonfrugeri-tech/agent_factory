from openai import OpenAI
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.database.mongo_db_client import MongoDBClient
from src.domain.vector import Vector
from src.domain.file import File


class VectorBusiness:
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.VECTOR_STORE_COLLECTION = "vector_store"
        self.FILE_COLLECTION = "files"

        self.openai = OpenAI()
        self.client_mongo_db = MongoDBClient(mongo_db=mongo_db)

    async def create_knowledge_base(self, name: str) -> str:
        vector_store = self.openai.vector_stores.create(name=name)
        vector_store_id = vector_store.id

        await self.client_mongo_db.create_document(
            collection_name=self.VECTOR_STORE_COLLECTION,
            document=Vector(
                id=vector_store_id,
                name=name,
            ).model_dump(),
        )

        return vector_store_id

    async def add_files(self, vector_store_id: str, file_ids: List[str]) -> None:
        try:
            vector_store_dict = await self.client_mongo_db.get_document(
                collection_name=self.VECTOR_STORE_COLLECTION, query={"id": vector_store_id}
            )

            if not vector_store_dict:
                raise ValueError(f"Vector store with id {vector_store_id} not found")

            vector_store = Vector(**vector_store_dict)

            if vector_store.files is None:
                vector_store.files = []

            for file_id in file_ids:
                file_dict = await self.client_mongo_db.get_document(
                    collection_name=self.FILE_COLLECTION, query={"id": file_id}
                )

                if not file_dict:
                    raise ValueError(f"File with id {file_id} not found")

                file = File(**file_dict)
                vector_store.files.append(file)

            await self.client_mongo_db.update_document(
                collection_name=self.VECTOR_STORE_COLLECTION,
                query={"id": vector_store_id},
                update={"files": [file.model_dump() for file in vector_store.files]},
            )
        except Exception as e:
            print(f"ERROR: {str(e)}")
            raise ValueError(str(e))

    def get_vector_files(self, vector_store_id: str) -> Dict[str, Any]:
        result = self.openai.vector_stores.files.list(vector_store_id=vector_store_id)
        return result.to_dict()
