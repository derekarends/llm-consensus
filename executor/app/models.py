
from pydantic import BaseModel


class ExecuteCommand(BaseModel):
    chat_id: str
    question: str