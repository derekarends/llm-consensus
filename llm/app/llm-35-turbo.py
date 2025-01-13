from openai import AzureOpenAI  
from app import settings

deployment = settings.azure_openai_deployment_name
client = AzureOpenAI(  
    azure_endpoint=settings.azure_openai_endpoint,  
    api_key=settings.azure_openai_api_key,  
    api_version=settings.azure_openai_api_version,  
)

#Prepare the chat prompt 
chat_prompt = [
    {
        "role": "system",
        "content": "You are an AI assistant that helps people find information."
    }
] 
    
# Include speech result if speech is enabled  
messages = chat_prompt  
    
# Generate the completion  
completion = client.chat.completions.create(  
    model=deployment,  
    messages=messages,  
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,  
    stop=None,  
    stream=False
)

print(completion.to_json())  
    