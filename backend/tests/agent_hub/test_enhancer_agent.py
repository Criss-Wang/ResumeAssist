from unittest.mock import patch, MagicMock
from resume_assist.agent_hub.enhancer_agent import EnhancerAgent
from resume_assist.engines.base_engine import BaseEngine


@patch("resume_assist.agent_hub.base.load_agent_config")
@patch("resume_assist.agent_hub.base.load_engine")
@patch("resume_assist.agent_hub.base.load_prompt")
def test_enhancer_agent_init(
    mock_load_prompt, mock_load_engine, mock_load_agent_config
):
    mock_engine_instance = MagicMock(spec=BaseEngine)
    mock_load_engine.return_value = lambda params, name: mock_engine_instance
    mock_load_agent_config.return_value = MagicMock()
    mock_load_prompt.return_value = MagicMock()

    agent = EnhancerAgent(task_name="enhance_task", use_prompt=True, prompt_version=1)

    assert agent.task_name == "enhance_task"
    assert agent.config == mock_load_agent_config.return_value
    assert agent.engine == mock_engine_instance
    assert agent.prompt == mock_load_prompt.return_value


@patch("resume_assist.agent_hub.base.load_agent_config")
@patch("resume_assist.agent_hub.base.load_engine")
@patch("resume_assist.agent_hub.base.load_prompt")
@patch("resume_assist.agent_hub.enhancer_agent.parse_to_bullet_pts")
@patch("resume_assist.agent_hub.enhancer_agent.parse_skill_pts")
def test_enhancer_agent_step(
    mock_parse_skill_pts,
    mock_parse_to_bullet_pts,
    mock_load_prompt,
    mock_load_engine,
    mock_load_agent_config,
):
    mock_engine_instance = MagicMock(spec=BaseEngine)
    mock_load_engine.return_value = lambda params, name: mock_engine_instance
    mock_load_agent_config.return_value = MagicMock()
    mock_load_prompt.return_value = MagicMock()
    mock_parse_to_bullet_pts.return_value = ["- point 1", "- point 2"]
    mock_parse_skill_pts.return_value = ["- point 1", "- point 2"]

    mock_engine_instance.run_instruction.return_value = "- point 1\n- point 2"

    agent = EnhancerAgent(task_name="work", use_prompt=True, prompt_version=1)

    input_vars = {"var1": "value1", "var2": "value2"}
    result = agent.step(input_vars)

    system_prompt = mock_load_prompt.return_value.system.value.format(**input_vars)
    user_prompt = mock_load_prompt.return_value.user.value.format(**input_vars)
    expected_messages = [
        ("system", system_prompt),
        ("user", user_prompt),
    ]

    mock_engine_instance.run_instruction.assert_called_once_with(expected_messages)
    mock_parse_to_bullet_pts.assert_called_once_with("- point 1\n- point 2")
    assert result == ["- point 1", "- point 2"]

    agent = EnhancerAgent(task_name="skills", use_prompt=True, prompt_version=1)
    result = agent.step(input_vars)
    assert result == ["- point 1", "- point 2"]


def test_enhancer_agent_get_agent_name():
    agent = EnhancerAgent(task_name="work", use_prompt=True, prompt_version=1)
    assert agent.get_agent_name() == "enhancer"


def test_enhancer_agent_no_prompt():
    agent = EnhancerAgent(task_name="work", use_prompt=False, prompt_version=1)
    assert agent.prompt is None
