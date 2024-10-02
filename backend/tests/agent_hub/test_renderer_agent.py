from unittest.mock import patch, MagicMock
from resume_assist.agent_hub.render_agent import RenderAgent
from resume_assist.engines.base_engine import BaseEngine


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

    input_vars = {
        "personal": {
            "name": "Full Name",
            "email": "youremail@yourdomain.com",
            "phone": "tel:+90-541-999-99-99",
            "website": "https://yourwebsite.com/",
            "social_networks": [
                {"network": "LinkedIn", "username": "yourusername"},
                {"network": "GitHub", "username": "yourusername"},
            ],
        },
        "education": {
            "education": [
                {
                    "institution": "University of Pennsylvania",
                    "area": "Computer Science",
                    "degree": "BS",
                    "start_date": "2000-09",
                    "end_date": "2005-05",
                    "highlights": [
                        "GPA: 3.9/4.0",
                        "**Coursework:** Computer Architecture, Comparison of Learning Algorithms, Computational Theory",
                    ],
                }
            ]
        },
        "work": {
            "experience": [
                {
                    "company": "Apple",
                    "position": "Software Engineer",
                    "location": "Cupertino, CA",
                    "start_date": "2005-06",
                    "end_date": "2007-08",
                    "highlights": ["a", "b", "c"],
                },
            ]
        },
        "skills": {
            "skills": [
                {"label": "Language", "details": "C++, Python"},
                {"label": "Tech", "details": "C++, Python"},
            ]
        },
        "projects": {
            "projects": [
                {
                    "name": "Multi-User Drawing Tool",
                    "date": "[code](https://github.com/sinaatalay/rendercv)",
                    "highlights": ["a", "b", "C"],
                }
            ]
        },
        "publications": {
            "publications": [
                {
                    "title": "3D Finite Element Analysis of No-Insulation Coils",
                    "authors": ["author 1", "author 2"],
                    "date": "NeurIPS 2022",
                }
            ]
        },
        "summary": {"Professional Summary": ["summary here"]},
    }

    assert agent.step(input_vars)
