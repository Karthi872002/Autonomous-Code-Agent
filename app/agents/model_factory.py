# app/models/factory.py

from enum import Enum
from langchain_core.language_models import BaseChatModel


class ModelProvider(str, Enum):
    NVIDIA = "nvidia"
    OPENAI = "openai"
    GROQ = "groq"
    GOOGLE = "google"


def create_model(provider: str, model: str, api_key: str) -> BaseChatModel:
    match ModelProvider(provider.lower()):

        case ModelProvider.NVIDIA:
            from langchain_nvidia_ai_endpoints import ChatNVIDIA
            return ChatNVIDIA(model=model, api_key=api_key)

        case ModelProvider.OPENAI:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=model, api_key=api_key)

        case ModelProvider.GROQ:
            from langchain_groq import ChatGroq
            return ChatGroq(model=model, api_key=api_key)

        case ModelProvider.GOOGLE:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model=model, google_api_key=api_key)

        case _:
            raise ValueError(f"Unsupported provider: {provider}")