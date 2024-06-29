import yaml

from resume_assist.app.config import PromptModel


def verify_prompt(prompt, name, version, engine, model):
    if prompt.name != name or prompt.version != version:
        return False
    if prompt.engine != engine and engine != "":
        return False
    if prompt.model != model and model != "":
        return False
    return True


def load_prompt(task_name, name, version, engine="", model=""):
    with open(f"prompts/{task_name}.yaml", "r+") as f:
        prompt_list = yaml.safe_load(f)
        for prompt in prompt_list:
            prompt = PromptModel.model_validate(prompt)
            if verify_prompt(prompt, name, version, engine, model):
                return prompt

    raise ValueError("Prompt not found")
