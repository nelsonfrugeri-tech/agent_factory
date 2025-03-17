import argparse
from openai import OpenAI

client = OpenAI()


def _retrieval_vector_and_files(id):
    vector_store = client.vector_stores.retrieve(vector_store_id=id)
    files = client.vector_stores.files.list(vector_store_id=id)
    return vector_store, files


def _retrieve(id: str):
    try:
        vector_store, files = _retrieval_vector_and_files(id)

        print(f"Vector Store: {vector_store.name}")
        for file in files:
            file_details = client.files.retrieve(file_id=file.id)
            print(
                f"ID do Arquivo: {file.id} - Nome do Arquivo: {file_details.filename}"
            )
    except Exception as e:
        print(f"Erro ao recuperar o vector store: {e}")


def _delete_files(vector_store_id):
    try:
        _, files = _retrieval_vector_and_files(id)

        files = client.files.list()
        for file in files.data:
            client.files.delete(file.id)
            print(f"ID: {file.id} excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir arquivos do vector_store '{vector_store_id}': {e}")


def _delete_vector_store(vector_store_id):
    try:
        client.vector_stores.delete(vector_store_id=vector_store_id)
        print(f"Vector store '{vector_store_id}' excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir o vector store '{vector_store_id}': {e}")


if __name__ == "__main__":
    while True:
        print("Escolha a operação:")
        print("1 - Retrieve VectorStore e Files")
        print("2 - Delete Files from VectorStore")
        print("0 - Exit")
        choice = input("Digite o número da operação: ")

        if choice == "1":
            vector_store_id = input("Digite o ID do vector store: ")
            _retrieve(vector_store_id)
        elif choice == "2":
            vector_store_id = input("Digite o ID do vector store: ")
            _delete_files(vector_store_id)
        elif choice == "3":
            vector_store_id = input("Digite o ID do vector store: ")
            _delete_vector_store(vector_store_id)
        elif choice == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
