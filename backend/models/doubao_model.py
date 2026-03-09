from .openai_compatible_model import OpenAICompatibleModel
import os

class DouBaoModel(OpenAICompatibleModel):
    def __init__(self):
        super().__init__(
            api_key=os.getenv("DOUBAO_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            model="doubao-vision-pro"
        )
