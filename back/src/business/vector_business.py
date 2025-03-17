from openai import OpenAI
from pydantic import UUID4
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.database.mongo_db_client import MongoDBClient
from src.domain.vector import Vector


class VectorBusiness:
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.VECTOR_STORE_COLLECTION = "vector_store"
        self.PROJECT_COLLECTION = "projects"

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

    async def add_project(self, vector_store_id: str, project_id: str) -> None:
        try:
            vector_store = await self.client_mongo_db.get_document(
                collection_name=self.VECTOR_STORE_COLLECTION,
                query={"id": vector_store_id},
            )

            if not vector_store:
                raise ValueError(f"Vector store with id {vector_store_id} not found")

            project = await self.client_mongo_db.get_document(
                collection_name=self.PROJECT_COLLECTION, query={"id": project_id}
            )

            for file in project["files"]:
                self.openai.vector_stores.files.create(
                    vector_store_id=vector_store_id,
                    file_id=file["id"],
                )

                print(
                    f'File {file["id"]} added to OpenAI vector store {vector_store_id}'
                )

            await self.client_mongo_db.update_document(
                collection_name=self.PROJECT_COLLECTION,
                query={"id": project_id},
                update={"$set": {"vector_store": vector_store}},
            )
        except Exception as e:
            print(f"ERROR: {str(e)}")
            raise ValueError(str(e))

    def get_vector_files(self, vector_store_id: str) -> Dict[str, Any]:
        result = self.openai.vector_stores.files.list(vector_store_id=vector_store_id)
        return result.to_dict()
