import os
from openai import OpenAI
import asyncio
from .base_model import BaseModel

class OpenAICompatibleModel(BaseModel):
    """Base class for models with OpenAI-compatible APIs"""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def generate_caption(self, image_base64: str, media_type: str):
        """Generate caption without streaming"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please provide a detailed caption for this image."},
                    {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_base64}"}}
                ]
            }],
            max_tokens=1024
        )
        return response.choices[0].message.content

    async def generate_caption_stream(self, image_base64: str, media_type: str):
        """Generate caption with streaming"""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please provide a detailed caption for this image."},
                    {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_base64}"}}
                ]
            }],
            max_tokens=1024,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
                await asyncio.sleep(0)
