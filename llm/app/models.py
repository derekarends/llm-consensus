import logging
from pydantic import BaseModel
from app import settings
from .gpt import execute as execute_gpt
from .phi import execute as execute_phi

logger = logging.getLogger(__name__)


class SearchCommand(BaseModel):
    chat_id: str
    question: str

    def execute(self):
        print(settings.llm)
        if settings.llm == "phi":
            res = execute_phi(chat_id=self.chat_id, question=self.question)
        else:
            res = execute_gpt(chat_id=self.chat_id, question=self.question)
        logging.info(f"Response: {res}")
        return res


class PromptCommand:
    prompt = ""
