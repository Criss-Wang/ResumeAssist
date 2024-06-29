from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EngineType(str, Enum):
    Anthropic = "anthropic"
    OpenAI = "openai"


class Message(BaseModel):
    value: str


class PromptModel(BaseModel):
    name: str
    engine: str = Field(default="global")
    model: str = Field(default="global")
    version: int = Field(default=1)
    system: Optional[Message]
    user: Message


class AppConfig(BaseModel):
    engine_type: EngineType
