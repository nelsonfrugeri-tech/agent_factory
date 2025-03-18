import openai
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from agents import Agent, Runner
from src.database.mongo_db_client import MongoDBClient
from src.model.request.chat_message_request import MessageRequest, ToolRequest
from src.domain.chat import Chat, Conversation, Question, Answer, Message, Tool
from src.tool.computer import start_process, execute_curl


class ChatBusiness:
    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.CHAT_COLLECTION = "chats"
        self.client_mongo_db = MongoDBClient(mongo_db=mongo_db)
        self.openai_client = openai.OpenAI()

        self.computer_use = Agent(
            name="Executor de processos e curl",
            instructions="Você deve executar os comandos abaixo para iniciar o processo e executar o curl.",
            model="o3-mini",
            tools=[execute_curl],
        )

    async def create(self, name: str, tools: List[ToolRequest]) -> Chat:
        chat = Chat(name=name)
        chat.tools = [Tool(type=tool.type, index=tool.index) for tool in tools]

        await self.client_mongo_db.create_document(
            collection_name=self.CHAT_COLLECTION,
            document=chat.model_dump(),
        )
        return chat

    async def message(
        self, uuid: str, message: MessageRequest, tools: List[ToolRequest]
    ) -> str:
        try:            
            chat_document = await self.client_mongo_db.get_document(
                collection_name=self.CHAT_COLLECTION,
                query={"id": uuid},
            )

            chat = Chat(**chat_document)

            new_question = Question(
                message=Message(role=message.role, content=message.content),
                tools=[Tool(type=tool.type, index=tool.index) for tool in tools],
            )
            chat.conversations.append(Conversation(question=new_question, answer=None))

            input_messages = [
                {
                    "role": conv.question.message.role,
                    "content": conv.question.message.content,
                }
                for conv in chat.conversations[-2:]
            ]
            input_messages.append({"role": message.role, "content": message.content})

            result = await Runner.run(self.computer_use, message.content)

            print(result.final_output)

            response = self.openai_client.responses.create(
                model="gpt-4o",
                input=input_messages,
                tools=[
                    {"type": tool.type, "vector_store_ids": tool.index}
                    for tool in tools
                ],
            )

            response_message = Message(
                role="assistant", content=response.output[1].content[0].text
            )

            chat.conversations[-1].answer = Answer(message=response_message)

            await self.client_mongo_db.update_document(
                collection_name=self.CHAT_COLLECTION,
                query={"id": uuid},
                update={
                    "$push": {"conversations": chat.conversations[-1].model_dump()}
                },
            )

            return response_message.content
        except Exception as e:
            print(f"Error on message: {e}")
            raise e

    async def get_all_chats(self) -> List[Chat]:
        chat_documents = await self.client_mongo_db.get_all_documents(
            collection_name=self.CHAT_COLLECTION
        )
        return [Chat(**doc) for doc in chat_documents]
