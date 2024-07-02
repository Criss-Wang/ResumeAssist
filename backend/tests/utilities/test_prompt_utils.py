from resume_assist.utilities.prompt_utils import load_prompt


def test_load_prompt():
    task_name = "work"
    name = "work_assist"
    version = 1
    engine = "global"
    model = "global"
    prompt = load_prompt(task_name, name, version, engine, model)
    assert prompt
    prompt = load_prompt(task_name, name, version)
    assert prompt


test_load_prompt()
