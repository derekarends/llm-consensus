import logging
from typing import List
from openai import AzureOpenAI
from app import settings


logger = logging.getLogger(__name__)

def execute(messages: List[dict]) -> str | None:    
    deployment = settings.azure_openai_deployment_name
    client = AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )

    completion = client.chat.completions.create(model=deployment, messages=messages) # type: ignore
    logger.info(f"Completion: {completion.choices[0].message.content}")
    return completion.choices[0].message.content
