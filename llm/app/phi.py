import logging
from typing import List
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import ChatCompletions
from azure.core.credentials import AzureKeyCredential
from app import settings

logger = logging.getLogger(__name__)


def execute(messages: List[dict]) -> str:
    client = ChatCompletionsClient(
        endpoint=settings.azure_openai_endpoint,
        credential=AzureKeyCredential(settings.azure_openai_api_key),
    )

    response: ChatCompletions = client.complete(messages=messages)  # type: ignore
    logger.info(f"Response: {response.choices[0].message.content}")

    return response.choices[0].message.content
