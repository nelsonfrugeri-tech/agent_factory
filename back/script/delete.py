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
#         "file-YX37jRwarE8qwZRwgpcGHn",
#         "file-FbW9Lh6rjPqmCtnuJm816j",
#         "file-LFJi9vZEc2TvArapo6Eyzg",
#         "file-kE04EmYyMXhWizw3tDhUPoYM",
#         "file-oVL50keI9QJuGMrYhkP0Wvdp",
#         "file-OTaVi3DBSgETdzNjIQajtNU2",
#         "file-d7snYgeAon8RWo7TXYWsUrhH",
#         "file-yqR4coasCQMAwCYgLdJrmpwX",
#         "file-4yRiqi9yf2ZOGyXTFl5EJT9S",
#         "file-0Xt14OEWbvfmFmit7wLCiHHp",
#         "file-hQiHaOTFlgNEQ0vbXubrpvvC",
#         "file-4o6756tzvVzstx29IGoXuOAT",
#         "file-U3ELwk4YeTd7YlkdaBBKN5D2",
#         "file-sJdHWsczrlqhSqQggpCBST1A",
#         "file-bX7SE90EJkyhVVwITFrTXq7o",
#         "file-bLUBcqHt96YiMD1o47T9uuOG",
#         "file-mZl3abhVR39ciNt9rOCPjaFF",
#         "file-Rrv3juM2aYAchsHswlHinF6c",
#         "file-qEsyZncNr930htsREHGzzoIH",
#         "file-bh34cBSqWWHuwsVmfGSPvTul",
#         "file-E6HPVTUZURBoiKqHkbRIgyvp",
#         "file-Je5pKI3b8QaYTDx33goCZP97",
#         "file-9OV8j80BFU1CiM97juI2DfRV",
#         "file-7hPLtz0rgl9rXK2i7fQoQwyu",
#         "file-9WjZgblaCv28bDjD7qZy6yKN",
#         "file-QoUjlt3FSEsxEkr63ZAnduMy",
#         "file-7w9UygHfUui54aBHtTFJ4bpw",
#         "file-GDKHEKWMMVpfTs1BmcGF4Ky7",
#         "file-VszqOnucZ1xEvHEqwWJWcOPg",
#         "file-fpfV47PLpQ1teLLqL2IOUtTg",
#         "file-RyFa1xhobBgiVkL7RDs36rsR",
#         "file-WffZgbfoWe83KIcJplyItctz",
#         "file-ldZs1Z5Y8xMizzZBydJrGsbO",
#         "file-xoMrEqqpVTn3V4WVVtknPTDW",
#         "file-Xl6xnkO94J8CTffZfEVdtrOt",
#         "file-wsRaujkav600rrg4AHeybB36",
#         "file-OP8N5ga0fvyZtgdj2tUMBlbZ",
#         "file-FogfhM0wtg6ILi7GscLLWd7W",
#         "file-oeAfZYA0yX6IhMV7RkXmEgzN",
#         "file-QeTfPSy4ofm3B2snjfpkLnUG",
#         "file-ca6VLBY4ckjkjg8BXcuxpD6g",
#         "file-3rLzGcU1zduEU499uYRljJPs",
#         "file-SmEBSWtkDnkRio88eSZf51gs",
#         "file-VTNFc98twWaP8iUCqFgrz4ie",
#         "file-cPAbJHMwReYEWcH4VLloqnSP",
#         "file-w6PyP5FB1JNYSdKUDaEb79nr",
#         "file-91IwFJSFciPTqRHQ3mO2OYXz",
#         "file-SlkfKXwsgmdpLOPJFfbyTVWn",
#         "file-lfeluIIRR17sii6bpJANxEET",
#         "file-qCsxKKIpdabMPtaaC0qXOGjT",
#         "file-8f8p1eiQNCdjZWzhWVTPhoon",
#         "file-PhmVl67PTep8OYe8J2Xc7fN7",
#         "file-1YDBvF2I2zrU3L17dlCBUHwD",
#         "file-Rai2Qh4K2Grm7qL8mnJRkKMY",
#         "file-76HtaHddpXn0OZsmWSxGuuEi",
#     ]
# )


list_and_print_all_files()
