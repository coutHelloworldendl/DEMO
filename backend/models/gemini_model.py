import os
import google.generativeai as genai
import asyncio
import base64
from io import BytesIO
from PIL import Image
from .base_model import BaseModel

class GeminiModel(BaseModel):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def _base64_to_image(self, image_base64: str):
        """Convert base64 string to PIL Image"""
        image_data = base64.b64decode(image_base64)
        return Image.open(BytesIO(image_data))

    async def generate_caption(self, image_base64: str, media_type: str):
        """Generate caption without streaming"""
        image = self._base64_to_image(image_base64)
        response = self.model.generate_content([
            "Please provide a detailed caption for this image.",
            image
        ])
        return response.text

    async def generate_caption_stream(self, image_base64: str, media_type: str):
        """Generate caption with streaming"""
        image = self._base64_to_image(image_base64)
        response = self.model.generate_content(
            ["Please provide a detailed caption for this image.", image],
            stream=True
        )

        for chunk in response:
            if chunk.text:
                yield f"data: {chunk.text}\n\n"
                await asyncio.sleep(0)
