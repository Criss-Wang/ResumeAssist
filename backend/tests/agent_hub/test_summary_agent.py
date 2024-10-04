from unittest.mock import patch, MagicMock
from resume_assist.agent_hub.summary_agent import SummaryAgent
from resume_assist.engines.base_engine import BaseEngine


@patch("resume_assist.agent_hub.base.load_agent_config")
@patch("resume_assist.agent_hub.base.load_engine")
@patch("resume_assist.agent_hub.base.load_prompt")
def test_summary_agent_init(mock_load_prompt, mock_load_engine, mock_load_agent_config):
    mock_engine_instance = MagicMock(spec=BaseEngine)
    mock_load_engine.return_value = lambda params, name: mock_engine_instance
    mock_load_agent_config.return_value = MagicMock()
    mock_load_prompt.return_value = MagicMock()

    agent = SummaryAgent(task_name="summary_task", use_prompt=True, prompt_version=1)

    assert agent.task_name == "summary_task"
    assert agent.config == mock_load_agent_config.return_value
    assert agent.engine == mock_engine_instance
    assert agent.prompt == mock_load_prompt.return_value


@patch("resume_assist.agent_hub.base.load_agent_config")
@patch("resume_assist.agent_hub.base.load_engine")
@patch("resume_assist.agent_hub.base.load_prompt")
@patch("resume_assist.agent_hub.summary_agent.build_skills_str")
@patch("resume_assist.agent_hub.summary_agent.build_work_str")
@patch("resume_assist.agent_hub.summary_agent.build_project_str")
def test_summary_agent_step(
    mock_build_project_str,
    mock_build_work_str,
    mock_build_skills_str,
    mock_load_prompt,
    mock_load_engine,
    mock_load_agent_config,
):
    mock_engine_instance = MagicMock(spec=BaseEngine)
    mock_load_engine.return_value = lambda params, name: mock_engine_instance
    mock_load_agent_config.return_value = MagicMock()
    mock_load_prompt.return_value = MagicMock()
    mock_build_skills_str.return_value = "Formatted Skills"
    mock_build_work_str.return_value = "Formatted Work"
    mock_build_project_str.return_value = "Formatted Projects"

    mock_engine_instance.run_instruction.return_value = "Output from engine"

    agent = SummaryAgent(task_name="self-intro", use_prompt=True, prompt_version=1)

    input_vars = {
        "description": "Job description here",
        "skills": {"category1": ["skill1", "skill2"]},
        "work_experiences": [
            {
                "work_company": "Company1",
                "work_role": "Role1",
                "start_date": "2020",
                "end_date": "2021",
                "highlights": ["highlight1"],
            }
        ],
        "project_experiences": [
            {
                "project_name": "Project1",
                "start_date": "2020",
                "end_date": "2021",
                "highlights": ["highlight1"],
            }
        ],
    }
    result = agent.step(input_vars)

    updated_input_vars = {
        "description": "Job description here\n\n",
        "skills": "Formatted Skills\n\n",
        "work_experiences": "Formatted Work\n\n",
        "project_experiences": "Formatted Projects\n\n",
    }

    system_prompt = mock_load_prompt.return_value.system.value.format(
        **updated_input_vars
    )
    user_prompt = mock_load_prompt.return_value.user.value.format(**updated_input_vars)
    expected_messages = [
        ("system", system_prompt),
        ("user", user_prompt),
    ]

    mock_engine_instance.run_instruction.assert_called_once_with(expected_messages)
    assert result == "Output from engine"

    agent.task_name = "other_task"
    result = agent.step(input_vars)
    assert result == "Output from engine"


def test_summary_agent_update_self_intro_inputs():
    agent = SummaryAgent(task_name="self-intro", use_prompt=True, prompt_version=1)

    input_vars = {
        "description": "Job description here",
        "skills": {"category1": ["skill1", "skill2"]},
        "work_experiences": [
            {
                "work_company": "Company1",
                "work_role": "Role1",
                "start_date": "2020",
                "end_date": "2021",
                "highlights": ["highlight1"],
            }
        ],
        "project_experiences": [
            {
                "project_name": "Project1",
                "start_date": "2020",
                "end_date": "2021",
                "highlights": ["highlight1"],
            }
        ],
    }

    with patch(
        "resume_assist.agent_hub.summary_agent.build_skills_str",
        return_value="Formatted Skills",
    ), patch(
        "resume_assist.agent_hub.summary_agent.build_work_str",
        return_value="Formatted Work",
    ), patch(
        "resume_assist.agent_hub.summary_agent.build_project_str",
        return_value="Formatted Projects",
    ):

        updated_vars = agent.update_self_intro_inputs(input_vars)

        expected_vars = {
            "description": "Job description here\n\n",
            "skills": "Formatted Skills\n\n",
            "work_experiences": "Formatted Work\n\n",
            "project_experiences": "Formatted Projects\n\n",
            'word_limit': 100
        }

        assert updated_vars == expected_vars


def test_summary_agent_get_agent_name():
    agent = SummaryAgent(task_name="self-intro", use_prompt=True, prompt_version=1)
    assert agent.get_agent_name() == "summary"
