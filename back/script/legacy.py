from openai import OpenAI

# Inicializa o cliente OpenAI
client = OpenAI()


def delete_files_by_id(file_ids):
    try:
        for file_id in file_ids:
            # Exclui o arquivo pelo ID
            client.files.delete(file_id)
            print(f"Arquivo com ID '{file_id}' excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir arquivos: {e}")


def delete_files_from_vector_store(vector_store_id):
    try:
        # Lista os arquivos no vector store
        files = client.files.list()
        for file in files.data:
            # Verifica se o arquivo está associado ao vector_store_id
            if (
                hasattr(file, "vector_store_id")
                and file.vector_store_id == vector_store_id
            ):
                file_id = file.id
                file_name = getattr(file, "filename", "N/A")
                # Exclui cada arquivo individualmente
                client.files.delete(file_id)
                print(f"Arquivo '{file_name}' (ID: {file_id}) excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir arquivos do vector_store '{vector_store_id}': {e}")


def delete_vector_store(vector_store_id):
    try:
        # Exclui o vector store
        client.vector_stores.delete(vector_store_id=vector_store_id)
        print(f"Vector store '{vector_store_id}' excluído com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir o vector store '{vector_store_id}': {e}")


def list_and_print_all_files():
    try:
        # Lista todos os arquivos
        files = client.files.list()
        for file in files.data:
            file_id = file.id
            file_name = getattr(file, "filename", "N/A")
            print(f"Arquivo '{file_name}' (ID: {file_id})")
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")


# ID do vector store que você deseja excluir
vector_store_id = "vs_67d4741dbbe48191a008b78dd607d510"

# Executa as funções de exclusão
# delete_files_from_vector_store(vector_store_id)
# delete_vector_store(vector_store_id)

# delete_files_by_id(
#     [
#     ]
# )


list_and_print_all_files()
