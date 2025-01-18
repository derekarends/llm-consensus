import logging

from typing import List
from pydantic import BaseModel
from app import settings
from .redis_client import RedisClient
from .gpt import execute as execute_gpt
from .phi import execute as execute_phi

logger = logging.getLogger(__name__)


class SearchCommand(BaseModel):
    chat_id: str
    question: str

    def build_history(self) -> List[dict]:
        r = RedisClient()
        memory = r.get(self.chat_id) or []

        history = [
            {"role": "system", "content": "You are an AI assistant that specializes in kubernetes commands. Please ask me a question or give me a command. Limit the response to commands needed to complete the task."},
        ]
        for message in memory:  # type: ignore
            if message["role"] == "user":
                history.append({"role": "user", "content": message["content"] if "content" in message else ""})
            elif message["role"] == "assistant":
                history.append({"role": "assistant", "content": message["content"] if "content" in message else ""})

        history.append({"role": "user", "content": self.question})
        return history

    def execute(self):
        print(settings.llm)
        if settings.llm == "phi":
            res = execute_phi(self.build_history())
        else:
            res = execute_gpt(self.build_history())
        logging.info(f"Response: {res}")
        return res


class PromptCommand:
    prompt = ""
