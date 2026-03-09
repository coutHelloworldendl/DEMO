from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
from pathlib import Path
from dotenv import load_dotenv
import base64
from models.anthropic_model import AnthropicModel
from models.openai_model import OpenAIModel
from models.gemini_model import GeminiModel
from models.kimi_model import KimiModel
from models.doubao_model import DouBaoModel
from models.glm_model import GLMModel
from models.minimax_model import MinimaxModel
from models.grok_model import GrokModel

load_dotenv()

app = FastAPI(title="Image Captioning API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize models
models = {
    "claude-3-5-sonnet": AnthropicModel(),
    "gpt-4-vision": OpenAIModel(),
    "gemini-1.5-pro": GeminiModel(),
    "moonshot-v1-8k": KimiModel(),
    "doubao-vision-pro": DouBaoModel(),
    "glm-4v": GLMModel(),
    "minimax-vision-01": MinimaxModel(),
    "grok-vision-beta": GrokModel(),
}

@app.get("/")
async def root():
    return {"message": "Image Captioning API", "status": "running"}

@app.get("/models")
async def get_models():
    """Get list of available models"""
    return {
        "models": [
            {
                "id": "claude-3-5-sonnet",
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "supports_streaming": True
            },
            {
                "id": "gpt-4-vision",
                "name": "GPT-4 Vision",
                "provider": "OpenAI",
                "supports_streaming": True
            },
            {
                "id": "gemini-1.5-pro",
                "name": "Gemini 1.5 Pro",
                "provider": "Google",
                "supports_streaming": True
            },
            {
                "id": "moonshot-v1-8k",
                "name": "Kimi Vision",
                "provider": "Moonshot AI",
                "supports_streaming": True
            },
            {
                "id": "doubao-vision-pro",
                "name": "DouBao Vision Pro",
                "provider": "ByteDance",
                "supports_streaming": True
            },
            {
                "id": "glm-4v",
                "name": "GLM-4V",
                "provider": "Zhipu AI",
                "supports_streaming": True
            },
            {
                "id": "minimax-vision-01",
                "name": "Minimax Vision",
                "provider": "Minimax",
                "supports_streaming": True
            },
            {
                "id": "grok-vision-beta",
                "name": "Grok Vision",
                "provider": "xAI",
                "supports_streaming": True
            }
        ]
    }

@app.post("/caption")
async def caption_image(
    file: UploadFile = File(...),
    model_id: str = Form(...),
    stream: bool = Form(True)
):
    """Generate caption for uploaded image"""
    if model_id not in models:
        raise HTTPException(status_code=400, detail=f"Model {model_id} not supported")

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image data
    image_data = await file.read()

    # Encode to base64
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    # Get model instance
    model = models[model_id]

    if stream:
        # Return streaming response
        return StreamingResponse(
            model.generate_caption_stream(image_base64, file.content_type),
            media_type="text/event-stream"
        )
    else:
        # Return complete response
        caption = await model.generate_caption(image_base64, file.content_type)
        return {"caption": caption}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
