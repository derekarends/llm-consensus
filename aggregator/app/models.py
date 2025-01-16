
from pydantic import BaseModel


class SearchCommand(BaseModel):
    chat_id: str
    question: str