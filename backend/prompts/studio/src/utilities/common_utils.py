import re
import yaml
import random
from logging import config as logging_config
from typing import Dict

import numpy as np

from src.app.configs import OptConfig


def initialize_logging():
    with open("logging_config.yaml") as f:
        config_description = yaml.safe_load(f)
        logging_config.dictConfig(config_description)


def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)


def load_config(config_path):
    with open(file=config_path, mode="r+") as f:
        return OptConfig(**yaml.safe_load(f))


def flatten_dict(d: Dict, parent_key: str = "", sep: str = "_") -> Dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def parse_score_content(content: str) -> Dict:
    content = content.strip()
    pattern = r"<score>(.*?)</score>"
    match = re.search(pattern, content)
    if match:
        score = int(match.group(1))
    else:
        score = 0

    pattern = r"<reason>(.*?)</reason>"
    match = re.search(pattern, content)
    if match:
        reason = match.group(1)
    else:
        reason = "parsing error, check <reason> tag"

    return {"reason": reason, "score": score}
