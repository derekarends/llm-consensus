import logging

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.kernel import Kernel

from app import settings
from .redis_client import RedisClient

NAME = "Jeeves"
INSTRUCTIONS = """
You are an AI assistant specialized in determining if the user is asking a question or giving a Kubernetes command.
"""


async def invoke_agent(chat_id: str, question: str) -> str | None:
    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        service_id="agent",
        deployment_name=settings.azure_openai_deployment_name,
        api_key=settings.azure_openai_api_key,
        endpoint=settings.azure_openai_endpoint,
    )
    kernel.add_service(service=chat_completion)

    agent = ChatCompletionAgent(
        service_id="agent",
        kernel=kernel,
        name=NAME,
        instructions=INSTRUCTIONS,
    )

    r = RedisClient()
    memory = r.get(chat_id) or []

    history = ChatHistory()
    for message in memory:  # type: ignore
        if message["role"] == "user":
            history.add_user_message(message["content"] if "content" in message else "")
        elif message["role"] == "assistant":
            history.add_assistant_message(message["content"] if "content" in message else "")

    history.add_user_message(question)

    res = "I am sorry, I am not sure what you are asking. Please try again."

    async for content in agent.invoke(history):
        logging.info(f"Agent: {content.content}")
        res = content.content

    return res
