from typing import List, Dict

from langfuse.decorators import observe, langfuse_context
from langchain_anthropic import ChatAnthropic

from resume_assist.engines.base_engine import BaseEngine


class AnthropicEngine(BaseEngine):
    def init_model(self, model_params: Dict, model_name: str):
        if "claude" not in model_name:
            raise ValueError("invalid model")
        return ChatAnthropic(model_name=model_name, max_retries=3, **model_params)

<<<<<<< HEAD
=======
    @observe(as_type="generation")
>>>>>>> e8e1246 (update langfuse integration (cloud version))
    def run_instruction(self, messages: List):
        try:
            messages = [
                ("human" if role == "user" else role, content)
                for role, content in messages
            ]
            response = self.model.invoke(messages)
<<<<<<< HEAD
=======
            usage = response.response_metadata["usage"]
            langfuse_context.update_current_observation(
                input=messages,
                model=self.model_name,
                metadata=self.model_params,
                usage={
                    "input": usage["input_tokens"],
                    "output": usage["output_tokens"],
                },
            )
>>>>>>> e8e1246 (update langfuse integration (cloud version))
            return response.content
        except Exception as e:
            print(e)
            raise e

    def get_engine_str(self):
        return "Anthropic"
