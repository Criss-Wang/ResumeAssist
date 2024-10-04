from unittest.mock import patch, MagicMock
from resume_assist.agent_hub.render_agent import RenderAgent
from resume_assist.engines.base_engine import BaseEngine

FULL_PAYLOAD = {
    "id": "b9641efd-6b3a-4090-9be4-9916f40666f7",
    "job_details": {
        "position": "fdas",
        "company": "fdsa",
        "url": "fdas",
        "description": "fasfdsadf",
    },
    "personal_info": {
        "name": "fda",
        "email": "test@test.com",
        "linkedin": "https://www.linkedin.com/in/zhenlin-wang/",
        "github": "https://github.com/Criss-Wang",
        "phone": "+86 13900000000",
        "website": "www.google.com",
    },
    "researches": [
        {"title": "fdsa", "authors": "fdsafsa", "conference": "fdsa", "date": "08/2024"}
    ],
    "educations": [
        {
            "institution": "fda",
            "area": "fdsafsadf",
            "degree": "dadsafdsaf",
            "current": True,
            "gpa": "fdsafdsa",
            "courses": "fdafsaf",
            "other": "fdsafas;fdsafdsafafdsa",
            "start_date": "07/2024",
            "end_date": "",
        }
    ],
    "self_intro": {"content": "fdafdsafds", "title": "fdsa-fdas"},
    "skills": {
        "categories": ["New Category 1"],
        "skill_mapping": {"New Category 1": ["New Skill 1", "New Skill 2"]},
    },
    "work": [
        {
            "id": 1,
            "company": "fdsa",
            "role": "df",
            "location": "fdafsa",
            "start_date": "01/2024",
            "end_date": "08/2024",
            "current": False,
            "highlights": ["new highlight"],
        }
    ],
    "projects": [
        {
            "id": 1,
            "project_name": "llm-benchmark",
            "start_date": "Invalid Date",
            "end_date": "",
            "url": "fdsafsa",
            "current": True,
            "highlights": ["new highlight"],
        }
    ],
    "additional_info": {},
}


@patch("resume_assist.agent_hub.base.load_agent_config")
@patch("resume_assist.agent_hub.base.load_engine")
def test_summary_agent_init(mock_load_engine, mock_load_agent_config):
    mock_engine_instance = MagicMock(spec=BaseEngine)
    mock_load_engine.return_value = lambda params, name: mock_engine_instance
    mock_load_agent_config.return_value = MagicMock()

    agent = RenderAgent(task_name="render", use_prompt=False)

    assert agent.task_name == "render"
    assert agent.config == mock_load_agent_config.return_value
    assert agent.engine == mock_engine_instance


@patch("resume_assist.agent_hub.base.load_agent_config")
@patch("resume_assist.agent_hub.base.load_engine")
def test_summary_agent_step(
    mock_load_engine,
    mock_load_agent_config,
):
    mock_engine_instance = MagicMock(spec=BaseEngine)
    mock_load_engine.return_value = lambda params, name: mock_engine_instance
    mock_load_agent_config.return_value = MagicMock()

    mock_engine_instance.run_instruction.return_value = "Output from engine"

    agent = RenderAgent(task_name="render", use_prompt=False)

    input_vars = FULL_PAYLOAD

    assert agent.step(input_vars)

    input_vars["self_intro"] = {}
    input_vars["projects"] = []
    input_vars["researches"] = []
    input_vars["educations"] = []

    assert agent.step(input_vars)
