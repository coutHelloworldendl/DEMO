from .openai_compatible_model import OpenAICompatibleModel
import os

class GrokModel(OpenAICompatibleModel):
    def __init__(self):
        super().__init__(
            api_key=os.getenv("GROK_API_KEY"),
            base_url="https://api.x.ai/v1",
            model="grok-vision-beta"
        )
