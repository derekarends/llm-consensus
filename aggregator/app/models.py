from pydantic import BaseModel
from .llm_caller import invoke


class SearchCommand(BaseModel):
    chat_id: str
    question: str

    async def execute(self):
        return await invoke(self.chat_id, self.question)
