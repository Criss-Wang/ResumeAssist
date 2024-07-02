import yaml

from resume_assist.app.config import PromptModel


def verify_prompt(
    prompt: PromptModel, agent_name: str, version: int, engine: str, model: str
):
    if prompt.agent_name != agent_name or prompt.version != version:
        return False
    if prompt.engine != engine and engine != "":
        return False
    if prompt.model != model and model != "":
        return False
    return True


def load_prompt(
    section_name: str, agent_name: str, version: int, engine: str, model: str
):
    with open(f"prompts/{section_name}.yaml", "r+") as f:
        prompt_list = yaml.safe_load(f)
        for prompt in prompt_list:
            prompt = PromptModel.model_validate(prompt)
            if verify_prompt(prompt, agent_name, version, engine, model):
                return prompt

    raise ValueError("Prompt not found")
