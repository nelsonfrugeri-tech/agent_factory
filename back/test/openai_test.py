import openai


def main():
    client = openai.OpenAI()
    vector_store_id = (
        "vs_67d5f8fcfc2481919c56e2569bfba7fb"  # Substitua pelo seu vector_store_id
    )

    print("Chatbot iniciado. Digite 'exit' para sair.")
    while True:
        user_input = input("Você: ")
        if user_input.lower() == "exit":
            print("Encerrando o chatbot.")
            break

        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_input,
            tools=[{"type": "file_search", "vector_store_ids": [vector_store_id]}],
        )
        print("Chatbot:", response)


if __name__ == "__main__":
    main()
