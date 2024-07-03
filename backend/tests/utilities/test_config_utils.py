import pytest
from unittest.mock import mock_open, patch
import yaml
from resume_assist.app.config import AgentConfig
from resume_assist.utilities.config_utils import load_agent_config


@pytest.fixture
def mock_agent_config():
    return {
        "agent_1": {
            "engine_config": {
                "engine_type": "openai",
                "model_name": "model 1",
                "model_params": {},
            }
        }
    }


def test_load_agent_config_success(mock_agent_config):
    with patch("builtins.open", mock_open(read_data=yaml.dump(mock_agent_config))):
        with patch("yaml.safe_load", return_value=mock_agent_config):
            agent_config = load_agent_config("agent_1")
            assert agent_config.engine_config.engine_type == "openai"
            assert agent_config.engine_config.model_params == {}
            # Add assertions for other fields


def test_load_agent_config_not_found(mock_agent_config):
    with patch("builtins.open", mock_open(read_data=yaml.dump(mock_agent_config))):
        with patch("yaml.safe_load", return_value=mock_agent_config):
            with pytest.raises(
                ValueError,
                match="agent config not found in configuration file, please check your agent name",
            ):
                load_agent_config("non_existent_agent")
