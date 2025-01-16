import logging
from typing import List

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.contents import ChatMessageContent, ChatHistory
from semantic_kernel.kernel import Kernel

from __init__ import settings
from redis_client import RedisClient
from plugins import ExecutionPlugin, AggregatorPlugin


logger = logging.getLogger(__name__)


NAME = "Jeeves"
INSTRUCTIONS = """
You are an AI assistant specialized in determining if the user is asking a question or giving a Kubernetes command.
Your goal is to guide the user to help you determine if the user is asking a question or giving a command.
If you are unsure of what plugin to call, ask a follow-up question.
Otherwise, make a plan to respond to the user's question, then you will execute that plan by calling the appropriate plugin.
Return a string containing the response from the plugins.

Important Guidelines:
1. Never try to answer the question using your own knowledge.
2. Only call the 'aggregator' or 'executor' plugins and return their response.
3. Before calling the 'executor' plugin, ask the user for approval.

Example:
---
UserMessage:
{
    "content": "How do I create a pod running nginx?"
}

Plan:
1. Understand the user's intent.
2. Determine if the intent is clear or if a follow-up question is needed.
3. If the intent is clear, decide which plugin to call based on whether the user is asking a question or giving a command.
4. If the user is giving a command, ask for approval before calling the 'executor' plugin.
5. Call the appropriate plugin and return its response.
"""


def store_message(chat_id: str, message: List[ChatMessageContent]) -> None:
    r = RedisClient()
    memory = []
    for m in message:
        memory.append(m.to_dict())
    r.set(chat_id, memory)


async def invoke_agent(chat_id: str, question: str) -> str | None:
    kernel = Kernel()
    chat_completion = AzureChatCompletion(
        service_id="agent",
        deployment_name=settings.azure_openai_deployment_name,
        api_key=settings.azure_openai_api_key,
        endpoint=settings.azure_openai_endpoint,
    )
    kernel.add_service(service=chat_completion)
    execution_settings = kernel.get_prompt_execution_settings_from_service_id(service_id="agent")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    kernel.add_plugin(plugin=ExecutionPlugin(), plugin_name=ExecutionPlugin.name)
    kernel.add_plugin(plugin=AggregatorPlugin(), plugin_name=AggregatorPlugin.name)

    agent = ChatCompletionAgent(
        service_id="agent",
        kernel=kernel,
        name=NAME,
        instructions=INSTRUCTIONS,
        execution_settings=execution_settings,
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
    store_message(chat_id, history.messages)

    res = None
  
    async for content in agent.invoke(history):
        logger.info(f"Agent: {content.content}")
        res = content.content

    history.add_assistant_message(res)
    store_message(chat_id, history.messages)
    return res
