import pytest
from resume_assist.engines.anthropic_engine import AnthropicEngine
from resume_assist.app.config import EngineType
from resume_assist.engines.factories import load_engine


def test_load_engine_anthropic():
    engine = load_engine(EngineType.Anthropic)
    assert engine == AnthropicEngine


def test_load_engine_not_implemented():
    with pytest.raises(NotImplementedError):
        load_engine(EngineType("openai"))
    with pytest.raises(ValueError):
        load_engine(EngineType("Unknown"))
