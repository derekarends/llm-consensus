import logging
from semantic_kernel.contents import ChatHistory
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import ChatCompletions
from azure.core.credentials import AzureKeyCredential
from app import settings
from web.app.redis_client import RedisClient

logger = logging.getLogger(__name__)


def execute(chat_id: str, question: str) -> str:
    r = RedisClient()
    memory = r.get(chat_id) or []

    history = ChatHistory()
    for message in memory:  # type: ignore
        if message["role"] == "user":
            history.add_user_message(message["content"] if "content" in message else "")
        elif message["role"] == "assistant":
            history.add_assistant_message(message["content"] if "content" in message else "")

    history.add_user_message(question)

    client = ChatCompletionsClient(
        endpoint=settings.azure_openai_endpoint,
        credential=AzureKeyCredential(settings.azure_openai_api_key),
        history=history,
    )

    payload = {
        "messages": [
            {"role": "user", "content": question},
        ],
    }
    response: ChatCompletions = client.complete(payload)  # type: ignore
    logger.info(f"Response: {response.choices[0].message.content}")

    return response.choices[0].message.content
