import zipfile
from openai import OpenAI
from io import BytesIO
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.domain.file import Project, File
from src.database.mongo_db_client import MongoDBClient


class FileBusiness:
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.openai = OpenAI()
        self.client_mongo_db = MongoDBClient(mongo_db=mongo_db)

        self.MAX_FILE_SIZE_MB = 512
        self.SUPPORTED_EXTENSIONS = {
            ".txt",
            ".pdf",
            ".docx",
            ".xlsx",
            ".pptx",
            ".py",
            ".java",
            ".js",
            ".html",
            ".css",
        }

    def _call_openai(self, file_content: BytesIO, file_name: str) -> str:
        file_tuple: tuple[str, BytesIO] = (file_name, file_content)

        print(
            f"Uploading file: {file_name} with size: {len(file_content.getvalue())} bytes"
        )
        result = self.openai.files.create(file=file_tuple, purpose="assistants")

        print(result.id)
        return result.id

    async def create_project(self, zip_content: BytesIO, project_name: str) -> Project:
        try:
            zip_content.seek(0)
            files: List[File] = []

            zip_size_mb = len(zip_content.getvalue()) / (1024 * 1024)
            if zip_size_mb > self.MAX_FILE_SIZE_MB:
                raise ValueError(
                    f"ZIP file exceeds the maximum size of {self.MAX_FILE_SIZE_MB}MB"
                )

            project = Project(name=project_name)

            with zipfile.ZipFile(zip_content) as zip_file:
                for file_name in zip_file.namelist():
                    if not any(
                        file_name.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS
                    ):
                        print(f"Skipping unsupported file: {file_name}")
                        continue

                    with zip_file.open(file_name) as extracted_file:
                        file_content = BytesIO(extracted_file.read())
                        file_size_mb = len(file_content.getvalue()) / (1024 * 1024)

                        if file_size_mb > self.MAX_FILE_SIZE_MB:
                            print(f"Skipping large file: {file_name}")
                            continue

                        file_id = self._call_openai(file_content, file_name)
                        file = File(id=file_id, name=file_name)
                        files.append(file)

                        project.files.append(file)

            await self.client_mongo_db.create_document("projects", project.model_dump())

            return project
        except Exception as e:
            print(f"Error while creating project: {e}")
            raise e
