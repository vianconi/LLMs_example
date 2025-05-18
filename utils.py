import os
import yaml
from langchain_community.chat_models import ChatOpenAI
from typing import Optional
from pydantic import BaseModel

config = yaml.safe_load(open("config.yml"))

os.environ["OPENROUTER_API_KEY"] = config["OPENROUTER_API_KEY"]
os.environ["LANGCHAIN_API_KEY"] = config["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = str(config["LANGCHAIN_TRACING_V2"]).lower()
os.environ["LANGCHAIN_ENDPOINT"] = config["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_PROJECT"] = config["LANGCHAIN_PROJECT"]
os.environ["LANGCHAIN_HUB_API_KEY"] = config["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_HUB_API_URL"] = config["LANGCHAIN_HUB_API_URL"]
os.environ["SEACHAPI_API_KEY"] = config["SEACHAPI_API_KEY"]


class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: Optional[str]
    model_name: str

    def __init__(self,
                 model_name: str,
                 openai_api_key: Optional[str] = None,
                 openai_api_base: str = "https://openrouter.ai/api/v1",
                 **kwargs):
        openai_api_key = openai_api_key or os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name, **kwargs)
        