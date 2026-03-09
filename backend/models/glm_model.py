import os
from zhipuai import ZhipuAI
import asyncio
from .base_model import BaseModel

class GLMModel(BaseModel):
    def __init__(self):
        self.client = ZhipuAI(api_key=os.getenv("GLM_API_KEY"))
        self.model = "glm-4v"

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
            }]
        )
        return response.choices[0].message.content

    async def generate_caption_stream(self, image_base64: str, media_type: str):
        """Generate caption with streaming"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please provide a detailed caption for this image."},
                    {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_base64}"}}
                ]
            }],
            stream=True
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
                await asyncio.sleep(0)
