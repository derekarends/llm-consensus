from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import ChatCompletions
from azure.core.credentials import AzureKeyCredential
from app import settings


def execute():
    client = ChatCompletionsClient(
        endpoint=settings.azure_openai_endpoint,
        credential=AzureKeyCredential(settings.azure_openai_api_key),
    )

    model_info = client.get_model_info()
    print("Model name:", model_info.model_name)
    print("Model type:", model_info.model_type)
    print("Model provider name:", model_info.model_provider_name)

    payload = {
        "messages": [
            {"role": "user", "content": "I am going to Paris, what should I see?"},
            {
                "role": "assistant",
                "content": "Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:\n\n1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.\n2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.\n3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.\n\nThese are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world.",
            },
            {"role": "user", "content": "What is so great about #1?"},
        ],
        "max_tokens": 2048,
        "temperature": 0.8,
        "top_p": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    response: ChatCompletions = client.complete(payload)  # type: ignore

    print("Response:", response.choices[0].message.content)
    print("Model:", response.model)
    print("Usage:")
    print("	Prompt tokens:", response.usage.prompt_tokens)
    print("	Total tokens:", response.usage.total_tokens)
    print("	Completion tokens:", response.usage.completion_tokens)
