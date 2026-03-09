from .openai_compatible_model import OpenAICompatibleModel
import os

class KimiModel(OpenAICompatibleModel):
    def __init__(self):
        super().__init__(
            api_key=os.getenv("KIMI_API_KEY"),
            base_url="https://api.moonshot.cn/v1",
            model="moonshot-v1-8k"
        )
