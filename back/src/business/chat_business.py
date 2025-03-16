import openai
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.database.mongo_db_client import MongoDBClient
from src.model.request.chat_message_request import MessageRequest, ToolRequest
from src.domain.chat import Chat, Conversation, Question, Answer, Message, Tool


class ChatBusiness:
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.CHAT_COLLECTION = "chats"
        self.client_mongo_db = MongoDBClient(mongo_db=mongo_db)
        self.openai_client = openai.OpenAI()

    async def create(self, name: str) -> Chat:
        chat = Chat(name=name)
        await self.client_mongo_db.create_document(
            collection_name=self.CHAT_COLLECTION,
            document=chat.model_dump(),
        )
        return chat

    async def message(
        self, uuid: str, messages: List[MessageRequest], tools: List[ToolRequest]
    ) -> str:
        # Formatando ferramentas para o OpenAI
        tools_formatted = [
            {"type": tool.type, "vector_store_ids": tool.index} for tool in tools
        ]

        # Chamando a API da OpenAI
        response = self.openai_client.responses.create(
            model="gpt-4o-mini",
            input=messages[-1].content,
            tools=tools_formatted,
        )

        # Criando a resposta com o formato correto
        response_message = Message(
            role="assistant", content=response.output[1].content[0].text
        )

        # Construindo o objeto Conversation
        conversation = Conversation(
            question=Question(
                messages=[
                    Message(role=msg.role, content=msg.content) for msg in messages
                ],
                tools=[Tool(type=tool.type, index=tool.index) for tool in tools],
            ),
            answer=Answer(message=response_message),
        )

        # Atualizando o documento no MongoDB
        await self.client_mongo_db.update_document(
            collection_name=self.CHAT_COLLECTION,
            query={"id": uuid},
            update={"conversation": conversation.model_dump()}
        )

        return response_message.content
