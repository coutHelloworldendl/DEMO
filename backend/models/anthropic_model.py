import os
from anthropic import Anthropic
import asyncio

class AnthropicModel:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

    async def generate_caption(self, image_base64: str, media_type: str):
        """Generate caption without streaming"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Please provide a detailed caption for this image."
                        }
                    ],
                }
            ],
        )
        return message.content[0].text

    async def generate_caption_stream(self, image_base64: str, media_type: str):
        """Generate caption with streaming"""
        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Please provide a detailed caption for this image."
                        }
                    ],
                }
            ],
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\n\n"
                await asyncio.sleep(0)  # Allow other tasks to run
