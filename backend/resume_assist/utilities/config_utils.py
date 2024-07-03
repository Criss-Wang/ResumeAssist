import yaml  # type: ignore[import-untyped]

from resume_assist.app.config import AgentConfig


def load_agent_config(agent_name: str) -> AgentConfig:
    with open("configs/agents-config.yaml", "r+") as f:
        agent_config_map = yaml.safe_load(f)
    if agent_name not in agent_config_map:
        raise ValueError(
            "agent config not found in configuration file, please check your agent name"
        )
    return AgentConfig(**agent_config_map[agent_name])
