import logging
import aiohttp
import asyncio

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.kernel import Kernel

from app import settings
from .redis_client import RedisClient

logger = logging.getLogger(__name__)

NAME = "Jeeves"
INSTRUCTIONS = """
You are an AI assistant specialized in determining if the user is asking a question or giving a Kubernetes command.
"""


async def call_llm_service(
    session: aiohttp.ClientSession, service_host: str, payload: dict
) -> str:
    url = f"{service_host}/search"
    try:
        async with session.post(url, json=payload) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        logger.error(f"Error calling {service_host}: {e}")
        return str(e)


async def call_all_llms(payload: dict):
    services = ["llm-mini", "llm-turbo", "llm-phi"]
    urls = [f"http://{services[0]}:9001", f"http://{services[1]}:9002", f"http://{services[2]}:9003"]
    async with aiohttp.ClientSession() as session:
        tasks = [call_llm_service(session, url, payload) for url in urls]
        results = await asyncio.gather(*tasks)
    return dict(zip(services, results))


async def invoke(chat_id: str, question: str) -> str | None:
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

    llm_results = await call_all_llms({"chat_id": chat_id, "question": question})
    for service, result in llm_results.items():
        history.add_assistant_message(f"{service}: {result}")

    res = "I am sorry, I am not sure what you are asking. Please try again."

    async for content in agent.invoke(history):
        logging.info(f"Agent: {content.content}")
        res = content.content

    return res
