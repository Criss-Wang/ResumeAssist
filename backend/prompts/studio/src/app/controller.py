import concurrent
from tqdm import tqdm

import textgrad as tg
import numpy as np


def eval_sample(item, eval_fn, model):
    """
    This function allows us to evaluate if an answer to a question in the prompt is a good answer.

    """
    x, y = item
    x = tg.Variable(
        x, requires_grad=False, role_description="query to the language model"
    )
    y = tg.Variable(
        y, requires_grad=False, role_description="correct answer for the query"
    )
    response = model(x)
    try:
        eval_output_variable = eval_fn(
            inputs=dict(inputs=x, prediction=response, ground_truth_answer=y)
        )

        return int(eval_output_variable.value)
    except:
        eval_output_variable = eval_fn([x, y, response])
        eval_output_parsed = eval_fn.parse_output(eval_output_variable)
        return int(eval_output_parsed)


def eval_dataset(test_set, eval_fn, model, max_samples: int = None):
    if max_samples is None:
        max_samples = len(test_set)
    accuracy_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for _, sample in enumerate(test_set):

            future = executor.submit(eval_sample, sample, eval_fn, model)
            futures.append(future)
            if len(futures) >= max_samples:
                break
        tqdm_loader = tqdm(
            concurrent.futures.as_completed(futures), total=len(futures), position=0
        )
        for future in tqdm_loader:
            acc_item = future.result()
            accuracy_list.append(acc_item)
            tqdm_loader.set_description(f"Accuracy: {np.mean(accuracy_list)}")
    return accuracy_list


def run_validation_revert(system_prompt: tg.Variable, results, model, eval_fn, val_set):
    val_performance = np.mean(eval_dataset(val_set, eval_fn, model))
    previous_performance = np.mean(results["validation_acc"][-1])
    print("val_performance: ", val_performance)
    print("previous_performance: ", previous_performance)
    previous_prompt = results["prompt"][-1]

    if val_performance < previous_performance:
        print(f"rejected prompt: {system_prompt.value}")
        system_prompt.set_value(previous_prompt)
        val_performance = previous_performance

    results["validation_acc"].append(val_performance)


def train(train_loader, optimizer, model, eval_fn, system_prompt, val_set, test_set):
    results = {"test_acc": [], "prompt": [], "validation_acc": []}
    results["test_acc"].append(eval_dataset(test_set, eval_fn, model))
    results["validation_acc"].append(eval_dataset(val_set, eval_fn, model))
    results["prompt"].append(system_prompt.get_value())
    for epoch in range(3):
        for steps, (batch_x, batch_y) in enumerate(
            (pbar := tqdm(train_loader, position=0))
        ):
            pbar.set_description(f"Training step {steps}. Epoch {epoch}")
            optimizer.zero_grad()
            losses = []
            for x, y in zip(batch_x, batch_y):
                x = tg.Variable(
                    x,
                    requires_grad=False,
                    role_description="query to the language model",
                )
                y = tg.Variable(
                    y,
                    requires_grad=False,
                    role_description="correct answer for the query",
                )
                response = model(x)
                try:
                    eval_output_variable = eval_fn(
                        inputs=dict(
                            inputs=x, prediction=response, ground_truth_answer=y
                        )
                    )
                except:
                    eval_output_variable = eval_fn([x, y, response])
                losses.append(eval_output_variable)
            total_loss = tg.sum(losses)
            total_loss.backward()
            optimizer.step()

            run_validation_revert(system_prompt, results, model, eval_fn, val_set)

            print("sys prompt: ", system_prompt)
            test_acc = eval_dataset(test_set, eval_fn, model)
            results["test_acc"].append(test_acc)
            results["prompt"].append(system_prompt.get_value())
            if steps == 3:
                break

    return results
