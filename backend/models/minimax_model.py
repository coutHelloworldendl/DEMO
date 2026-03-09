from .openai_compatible_model import OpenAICompatibleModel
import os

class MinimaxModel(OpenAICompatibleModel):
    def __init__(self):
        super().__init__(
            api_key=os.getenv("MINIMAX_API_KEY"),
            base_url="https://api.minimax.chat/v1",
            model="minimax-vision-01"
        )
