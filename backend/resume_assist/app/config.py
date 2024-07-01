from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel, Field, ConfigDict


class EngineType(str, Enum):
    Anthropic = "anthropic"
    OpenAI = "openai"


class Message(BaseModel):
    value: str


class PromptModel(BaseModel):
    agent_name: str
    engine: str = Field(default="global")
    model: str = Field(default="global")
    version: int = Field(default=1)
    system: Optional[Message]
    user: Message


class EngineConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    engine_type: EngineType
    model_name: str
    model_params: Optional[Dict] = Field(default={})


class AgentConfig(BaseModel):
    engine_config: EngineConfig


class AppConfig(BaseModel):
    engine_type: EngineType
