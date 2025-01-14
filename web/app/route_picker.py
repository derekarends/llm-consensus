from openai import AzureOpenAI
from redis_client import RedisClient
from __init__ import settings

def call_aggregator(question: str) -> str:
    return "aggregator"

def call_executor(question: str) -> str:
    return "executor"

def execute(chat_id: str, question: str):
    deployment = settings.azure_openai_deployment_name
    client = AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )

    system_message = """
    You are an AI assistant specializing in determining if the user is asking a question or telling us a command.
    If the user is asking a qusetion you should return 'aggregator', 
    if the user is telling us a command you should return 'executor'.
    !Important: Never try to answer the qustion, only determine if it is a question or a command and return 'aggregator' or 'executor' accordingly.
    """
    system_message = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_message,
                }
            ],
        }
    ]

    r = RedisClient()
    history = r.get(chat_id) or []

    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": question,
            }
        ],
    }
    history.append(user_message) # type: ignore

    r.set(chat_id, history)
    chat_prompt = system_message + history # type: ignore

    messages = chat_prompt
    completion = client.chat.completions.create(model=deployment, messages=messages)  # type: ignore
    completion_dict = completion.to_dict()
    path: str = completion_dict["choices"][0]["message"]["content"] # type: ignore
    path = path.strip().lower()
    
    if path == "aggregator":
        res = call_aggregator(question)
    elif path == "executor":
        res = call_executor(question)
    else:
        res = "I am sorry, I am not sure what you are asking. Please try again."

    assistant_message = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": res,
            }
        ],
    }
    history.append(assistant_message) # type: ignore
    r.set(chat_id, history)

    print("history", history) 
    return res
