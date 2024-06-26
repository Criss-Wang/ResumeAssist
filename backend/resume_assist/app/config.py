from enum import Enum

from pydantic import BaseModel


class EngineType(str, Enum):
    Anthropic = "anthropic"
    OpenAI = "openai"


class AppConfig(BaseModel):
    engine_type: EngineType
