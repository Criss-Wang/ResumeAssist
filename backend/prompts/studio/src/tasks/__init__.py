import textgrad as tg
from textgrad.autograd.string_based_ops import StringBasedFunction

from .base import DataLoader
from src.app.configs import OptConfig
from src.tasks.rag_generation import RagGeneration, deep_eval_fn

AVAILABLE_DATASETS = [
    "RAG_generation",
]

AVAILABLE_INSTANCE_DATASETS = [
    "RAG_basic",
]


def load_task(config: OptConfig):
    """
    Args:
        task_name: the name of the task to evaluate
        evaluation_api: the engine to use for evaluation, if needed
    """
    if "sample" in config.task:
        # load data & components

        train_set = RagGeneration(f"datasets/{config.dataset}/train.csv")
        val_set = RagGeneration(f"datasets/{config.dataset}/val.csv")
        test_set = RagGeneration(f"datasets/{config.dataset}/test.csv")
        eval_fn = StringBasedFunction(deep_eval_fn, function_purpose=config.fn_purpose)

        STARTING_SYSTEM_PROMPT = train_set.get_task_description()
        train_loader = DataLoader(train_set, batch_size=3, shuffle=True)

        system_prompt = tg.Variable(
            STARTING_SYSTEM_PROMPT,
            requires_grad=True,
            role_description="structured system prompt to a somewhat capable language model that specifies the behavior and strategies for the QA task",
        )
        return train_loader, val_set, test_set, eval_fn, system_prompt

    else:
        raise ValueError(f"Task {config.task} not found.")
