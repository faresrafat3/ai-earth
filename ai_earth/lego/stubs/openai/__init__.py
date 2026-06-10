"""Stub for openai — lightweight replacement for import resolution."""

class OpenAI:
    def __init__(self, *args, **kwargs):
        self.chat = ChatNamespace()
        self.models = ModelsNamespace()

class AsyncOpenAI:
    def __init__(self, *args, **kwargs):
        self.chat = AsyncChatNamespace()

class ChatNamespace:
    def __init__(self):
        self.completions = ChatCompletions()

class AsyncChatNamespace:
    def __init__(self):
        self.completions = AsyncChatCompletions()

class ChatCompletions:
    def create(self, *args, **kwargs):
        raise NotImplementedError("openai stub — install openai for real usage")

class AsyncChatCompletions:
    async def create(self, *args, **kwargs):
        raise NotImplementedError("openai stub — install openai for real usage")

class ModelsNamespace:
    def list(self, *args, **kwargs):
        return []
