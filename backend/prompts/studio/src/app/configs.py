from enum import Enum
from typing import Any, List, Dict, Optional, Literal

from pydantic import BaseModel, ConfigDict


class OptConfig(BaseModel):
    eval_engine_name: str = "gpt-4o"
    test_engine_name: str = "gpt-3.5-turbo-0125"
    dataset: str = "sample"
    fn_purpose: str = (
        "The runtime of string-based function that checks if the answer to thq query is of high quality."
    )
    task: str = "sample"
