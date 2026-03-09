#!/usr/bin/env bash
# Quick stop script for the Image Captioning Demo
# Usage: chmod +x stop.sh && ./stop.sh

echo "Stopping backend..."
if command -v tmux >/dev/null 2>&1; then
  tmux kill-session -t caption-backend 2>/dev/null || true
fi
pkill -f "uvicorn main:app" 2>/dev/null || true

echo "Stopping frontend..."
if command -v tmux >/dev/null 2>&1; then
  tmux kill-session -t caption-frontend 2>/dev/null || true
fi
pkill -f "vite" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true

echo "Services stopped."
