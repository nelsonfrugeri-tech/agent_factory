from typing import List
from agents import Agent, FileSearchTool, Runner, WebSearchTool

class CoderAgent:
    def __init__(self, vector_store_ids: List[str]):
        self.agent = Agent(
            name="Assistant",
            tools=[
                WebSearchTool(),
                FileSearchTool(
                    max_num_results=3,
                    vector_store_ids=vector_store_ids,
                ),
            ],
        )
        
    async def run(self, messages: str) -> str:
        return await Runner.run(self.agent, messages)
