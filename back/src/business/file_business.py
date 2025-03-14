import zipfile
from openai import OpenAI
from io import BytesIO
from typing import List

class FileBusiness:
    def __init__(self):
        self.openai = OpenAI()
        self.MAX_FILE_SIZE_MB = 512
        self.SUPPORTED_EXTENSIONS = {'.txt', '.pdf', '.docx', '.xlsx', '.pptx', '.py', '.java', '.js', '.html', '.css'}

    def _call_openai(self, file_content: BytesIO, file_name: str) -> str:
        file_tuple: tuple[str, BytesIO] = (file_name, file_content)

        print(f"Uploading file: {file_name} with size: {len(file_content.getvalue())} bytes")
        result = self.openai.files.create(
            file=file_tuple,
            purpose="assistants"
        )

        print(result.id)
        return result.id
    
    def create_file(self, zip_content: BytesIO) -> List[str]:
        zip_content.seek(0)  # 🔥 Garante que o ponteiro está no início
        file_ids = []

        # ⚡ Validação do tamanho do arquivo ZIP
        zip_size_mb = len(zip_content.getvalue()) / (1024 * 1024)
        if zip_size_mb > self.MAX_FILE_SIZE_MB:
            raise ValueError(f"ZIP file exceeds the maximum size of {self.MAX_FILE_SIZE_MB}MB")

        # 🔥 Extrair o conteúdo do arquivo ZIP
        with zipfile.ZipFile(zip_content) as zip_file:
            for file_name in zip_file.namelist():
                if not any(file_name.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS):
                    print(f"Skipping unsupported file: {file_name}")
                    continue

                with zip_file.open(file_name) as extracted_file:
                    file_content = BytesIO(extracted_file.read())
                    file_size_mb = len(file_content.getvalue()) / (1024 * 1024)

                    if file_size_mb > self.MAX_FILE_SIZE_MB:
                        print(f"Skipping large file: {file_name}")
                        continue

                    # 🔥 Fazer o upload do arquivo real para a API da OpenAI
                    file_id = self._call_openai(file_content, file_name)
                    file_ids.append(file_id)

        return file_ids
    