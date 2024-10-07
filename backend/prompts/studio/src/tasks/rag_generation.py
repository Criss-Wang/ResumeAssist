import os
import json
import pandas as pd
import subprocess
import platformdirs
import textgrad as tg
from .base import Dataset
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from deepeval.test_case import LLMTestCase

# The below metric is taken from DSPy for consistenc
# and modified to work with TG-graphs


def deep_eval_fn(
    inputs: tg.Variable, prediction: tg.Variable, ground_truth_answer: tg.Variable
):
    correctness_metric = GEval(
        name="Correctness",
        model="gpt-4",
        criteria="Determine whether the actual output is factually correct based on the expected output.",
        # NOTE: you can only provide either criteria or evaluation_steps, and not both
        evaluation_steps=[
            "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
            "You should also heavily penalize omission of detail",
            "Vague language, or contradicting OPINIONS, are OK",
        ],
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    )

    test_case = LLMTestCase(
        input=str(inputs.value),
        actual_output=str(ground_truth_answer.value),
        expected_output=str(prediction.value),
    )

    correctness_metric.measure(test_case)

    # since only int is allowed, we multiply the loss by 100 to avoid convertion to 0
    return (
        int(correctness_metric.score * 100)
        if correctness_metric.score <= 1
        else correctness_metric.score
    )


class RagGeneration(Dataset):
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, index_col=0)
        self._task_description = "You will answer a user query using provided context. Analyze the query and context. Only output the answer as your answer."

    def get_task_description(self):
        return self._task_description

    def __getitem__(self, index):
        row = self.data.iloc[index]
        return row["x"], row["y"]

    def __len__(self):
        return len(self.data)

    def get_default_task_instruction(self):
        return self._task_description
