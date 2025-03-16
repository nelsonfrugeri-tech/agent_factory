from typing import Any, Dict, List
from motor.motor_asyncio import AsyncIOMotorDatabase


class MongoDBClient:
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo_db = mongo_db

    async def create_document(
        self, collection_name: str, document: Dict[str, Any]
    ) -> str:
        print(f"collection_name: {collection_name}")
        collection = self.mongo_db[collection_name]
        result = await collection.insert_one(document)
        print(f"result: {result}")
        return str(result.inserted_id)

    async def update_document(
        self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]
    ) -> int:
        collection = self.mongo_db[collection_name]
        result = await collection.update_one(query, update)
        return result.modified_count

    async def get_document(
        self, collection_name: str, query: Dict[str, Any]
    ) -> Dict[str, Any]:
        collection = self.mongo_db[collection_name]
        document = await collection.find_one(query)
        return document

    async def get_all_documents(self, collection_name: str) -> List[Dict[str, Any]]:
        collection = self.mongo_db[collection_name]
        documents = await collection.find().to_list(length=None)
        return documents
