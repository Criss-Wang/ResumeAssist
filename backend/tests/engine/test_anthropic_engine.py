import pytest
from unittest.mock import patch, MagicMock
from resume_assist.engines.anthropic_engine import AnthropicEngine


def test_real_run():
    model_params = {}
    model_name = "claude-3-5-sonnet-20240620"
    engine = AnthropicEngine(model_params, model_name)

    messages = [("user", "Hello"), ("assistant", "Hi there")]
    response = engine.run_instruction(messages)


@patch("resume_assist.engines.anthropic_engine.ChatAnthropic")
def test_anthropic_engine_init(mock_chat_anthropic):
    model_params = {"param1": "value1"}
    model_name = "claude-v1"

    engine = AnthropicEngine(model_params, model_name)

    mock_chat_anthropic.assert_called_once_with(
        model_name=model_name, max_retries=3, **model_params
    )
    assert engine.get_model() == model_name
    assert engine.get_engine_str() == "Anthropic"


@patch("resume_assist.engines.anthropic_engine.ChatAnthropic")
def test_anthropic_engine_invalid_model(mock_chat_anthropic):
    model_params = {"param1": "value1"}
    model_name = "invalid_model"

    with pytest.raises(ValueError, match="invalid model"):
        AnthropicEngine(model_params, model_name)


@patch("resume_assist.engines.anthropic_engine.ChatAnthropic")
def test_anthropic_engine_run_instruction(mock_chat_anthropic):
    model_params = {"param1": "value1"}
    model_name = "claude-v1"
    mock_model = MagicMock()
    mock_chat_anthropic.return_value = mock_model
    mock_model.invoke.return_value.content = "response_content"

    engine = AnthropicEngine(model_params, model_name)

    messages = [("user", "Hello"), ("assistant", "Hi there")]
    response = engine.run_instruction(messages)

    expected_messages = [("human", "Hello"), ("assistant", "Hi there")]
    mock_model.invoke.assert_called_once_with(expected_messages)
    assert response == "response_content"


@patch("resume_assist.engines.anthropic_engine.ChatAnthropic")
def test_anthropic_engine_run_instruction_exception(mock_chat_anthropic):
    model_params = {"param1": "value1"}
    model_name = "claude-v1"
    mock_model = MagicMock()
    mock_chat_anthropic.return_value = mock_model
    mock_model.invoke.side_effect = Exception("Invocation error")

    engine = AnthropicEngine(model_params, model_name)

    messages = [("user", "Hello"), ("assistant", "Hi there")]

    with pytest.raises(Exception, match="Invocation error"):
        engine.run_instruction(messages)
