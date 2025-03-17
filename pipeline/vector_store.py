import argparse
from openai import OpenAI

client = OpenAI()


def _show(vector_store_id: str):
    vector_store = client.vector_stores.retrieve(vector_store_id=vector_store_id)
    files = client.vector_stores.files.list(vector_store_id=vector_store_id)


    print(f"Vector Store: {vector_store.name}")
    for file in files:
        file_details = client.files.retrieve(file_id=file.id)
        print(f"ID do Arquivo: {file.id} - Nome do Arquivo: {file_details.filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve and display vector store details.")
    parser.add_argument("vector_store_id", type=str, help="The ID of the vector store to retrieve.")
    args = parser.parse_args()
    _show(args.vector_store_id)
