# Image Captioning Demo

A scalable web application for image captioning with support for multiple AI models and streaming responses.

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python FastAPI with streaming support
- **Features**: Image upload, model selection, real-time streaming captions

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
.
├── backend/          # Python FastAPI backend
│   ├── main.py      # API endpoints
│   ├── models/      # Model integrations
│   └── requirements.txt
├── frontend/         # React TypeScript frontend
│   ├── src/
│   └── package.json
└── README.md
```
