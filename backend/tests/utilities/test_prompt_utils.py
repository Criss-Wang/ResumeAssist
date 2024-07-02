import pytest
from unittest.mock import mock_open, patch
from resume_assist.utilities.prompt_utils import verify_prompt, load_prompt


# Mock PromptModel for testing
class MockPromptModel:
    def __init__(self, agent_name, version, engine, model):
        self.agent_name = agent_name
        self.version = version
        self.engine = engine
        self.model = model

    @staticmethod
    def model_validate(data):
        return MockPromptModel(**data)


def test_verify_prompt():
    prompt = MockPromptModel("agent1", 1, "engine1", "model1")

    assert verify_prompt(prompt, "agent1", 1, "engine1", "model1") == True
    assert verify_prompt(prompt, "agent1", 1, "engine1", "") == True
    assert verify_prompt(prompt, "agent1", 1, "", "model1") == True
    assert verify_prompt(prompt, "agent1", 1, "", "") == True
    assert verify_prompt(prompt, "agent2", 1, "engine1", "model1") == False
    assert verify_prompt(prompt, "agent1", 2, "engine1", "model1") == False
    assert verify_prompt(prompt, "agent1", 1, "engine2", "model1") == False
    assert verify_prompt(prompt, "agent1", 1, "engine1", "model2") == False


@patch("builtins.open", new_callable=mock_open)
def test_load_prompt_not_found(mock_open):
    with patch("yaml.safe_load", return_value=[]):
        with pytest.raises(ValueError, match="Prompt not found"):
            load_prompt("section", "agent1", 1, "engine1", "model1")


@patch("builtins.open", new_callable=mock_open)
def test_load_prompt_success(mock_open):
    with patch(
        "yaml.safe_load",
        return_value=[
            {
                "agent_name": "agent1",
                "version": 1,
                "engine": "engine1",
                "model": "model1",
                "system": {"value": "system_prompt"},
                "user": {"value": "user prompt"},
            }
        ],
    ):
        with patch("resume_assist.app.config.PromptModel", MockPromptModel):
            prompt = load_prompt("section", "agent1", 1, "engine1", "model1")
            assert prompt.agent_name == "agent1"
            assert prompt.version == 1
            assert prompt.engine == "engine1"
            assert prompt.model == "model1"
            assert prompt.system.value == "system_prompt"
            assert prompt.user.value == "user prompt"


@patch("builtins.open", new_callable=mock_open)
def test_load_prompt_no_match(mock_open):
    with patch(
        "yaml.safe_load",
        return_value=[
            {
                "agent_name": "agent2",
                "version": 1,
                "engine": "engine1",
                "model": "model1",
                "system": {"value": "system_prompt"},
                "user": {"value": "user prompt"},
            }
        ],
    ):
        with patch("resume_assist.app.config.PromptModel", MockPromptModel):
            with pytest.raises(ValueError, match="Prompt not found"):
                load_prompt("section", "agent1", 1, "engine1", "model1")
