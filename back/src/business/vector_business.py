from openai import OpenAI
from typing import List, Dict, Any


class VectorBusiness:
    def __init__(self):
        self.openai = OpenAI()

    def create_knowledge_base(self, name: str) -> str:
        vector_store = self.openai.vector_stores.create(
            name=name
        )
        return vector_store.id

    def add_files(self, vector_store_id: str, file_ids: List[str]) -> None:
        for file_id in file_ids:
            self.openai.vector_stores.files.create(
                vector_store_id=vector_store_id,
                file_id=file_id
            )

    def get_vector_files(self, vector_store_id: str) -> Dict[str, Any]:
        result = self.openai.vector_stores.files.list(
            vector_store_id=vector_store_id
        )
        return result.to_dict() 