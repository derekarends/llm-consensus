import logging
from openai import AzureOpenAI
from app import settings
from .redis_client import RedisClient
from semantic_kernel.contents import ChatHistory


logger = logging.getLogger(__name__)

def execute(chat_id: str, question: str) -> str | None:
    r = RedisClient()
    memory = r.get(chat_id) or []

    history = ChatHistory()
    for message in memory:  # type: ignore
        if message["role"] == "user":
            history.add_user_message(message["content"] if "content" in message else "")
        elif message["role"] == "assistant":
            history.add_assistant_message(message["content"] if "content" in message else "")

    history.add_user_message(question)
    
    deployment = settings.azure_openai_deployment_name
    client = AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )

    completion = client.chat.completions.create(model=deployment, messages=history) # type: ignore
    logger.info(f"Completion: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
