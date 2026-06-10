"""Stub for litellm — lightweight replacement for import resolution."""
import warnings

class CompletionResponse:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def completion(*args, **kwargs):
    raise NotImplementedError("litellm stub — install litellm for real usage")

def embedding(*args, **kwargs):
    raise NotImplementedError("litellm stub — install litellm for real usage")

class CustomStreamWrapper:
    def __init__(self, *args, **kwargs):
        pass
    def __iter__(self):
        return iter([])
    def __next__(self):
        raise StopIteration

def get_model_info(*args, **kwargs):
    return {}

def validate_environment(*args, **kwargs):
    return {"keys_in_environment": []}

class ModelResponse:
    def __init__(self, **kwargs):
        self.choices = kwargs.get("choices", [])
        self.model = kwargs.get("model", "")
        self.usage = kwargs.get("usage", None)
        self.id = kwargs.get("id", "")

class Usage:
    def __init__(self, prompt_tokens=0, completion_tokens=0, total_tokens=0):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens

class Choices:
    def __init__(self, message=None, finish_reason=None):
        self.message = message or Message()
        self.finish_reason = finish_reason

class Message:
    def __init__(self, content="", role="assistant", tool_calls=None):
        self.content = content
        self.role = role
        self.tool_calls = tool_calls
        self.function_call = None

def cost_per_token(*args, **kwargs):
    return (0.0, 0.0)

def model_cost(**kwargs):
    return {}

def register_model(*args, **kwargs):
    pass

def drop_params(*args, **kwargs):
    return False, kwargs.get("kwargs", {})
