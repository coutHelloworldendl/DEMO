from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract base class for all vision models"""

    @abstractmethod
    async def generate_caption(self, image_base64: str, media_type: str) -> str:
        """Generate caption without streaming"""
        pass

    @abstractmethod
    async def generate_caption_stream(self, image_base64: str, media_type: str):
        """Generate caption with streaming - yields SSE format"""
        pass
