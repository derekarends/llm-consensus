from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_openai_deployment_name: str
    azure_openai_api_key: str
    azure_openai_api_version: str
    azure_openai_endpoint: str
    redis_host: str
    redis_port: int
