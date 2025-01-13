import os
from .config import Settings
from .dot_env import load_env

load_env()

settings = Settings(
    azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
    azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview"),
    azure_openai_deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
    azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
    llm=os.getenv("LLM", ""),
    redis_host=os.getenv("REDIS_HOST", "redis.service"),
    redis_port=int(os.getenv("REDIS_PORT", 6379)),
)
