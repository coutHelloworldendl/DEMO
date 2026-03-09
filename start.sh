#!/usr/bin/env bash
# Quick start script for the Image Captioning Demo
# Usage: chmod +x start.sh && ./start.sh

set -euo pipefail

# Start backend in a new terminal using tmux if available, otherwise in background
start_backend() {
  echo "Starting backend..."
  if command -v tmux >/dev/null 2>&1; then
    if tmux has-session -t caption-backend 2>/dev/null; then
      echo "tmux session 'caption-backend' already exists, leaving it running"
    else
      tmux new-session -d -s caption-backend "cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000"
      echo "Backend running in tmux session 'caption-backend'"
    fi
  else
    (cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000) &
    echo "Backend started in background"
  fi
}

# Start frontend in a new terminal using tmux if available, otherwise in background
start_frontend() {
  echo "Starting frontend..."
  if command -v tmux >/dev/null 2>&1; then
    if tmux has-session -t caption-frontend 2>/dev/null; then
      echo "tmux session 'caption-frontend' already exists, leaving it running"
    else
      tmux new-session -d -s caption-frontend "cd frontend && npm install && npm run dev"
      echo "Frontend running in tmux session 'caption-frontend'"
    fi
  else
    (cd frontend && npm install && npm run dev) &
    echo "Frontend started in background"
  fi
}

# Ensure virtualenv exists
if [ ! -d "backend/venv" ]; then
  echo "Creating Python virtual environment..."
  cd backend
  python -m venv venv
  echo "Run 'source backend/venv/bin/activate' before using Python commands."
  cd -
fi

# Run both services
start_backend

# if frontend port is in use, warn or let user override
check_port() {
  local port="$1";
  if command -v lsof >/dev/null 2>&1; then
    if lsof -iTCP:"$port" -sTCP:LISTEN -t >/dev/null 2>&1; then
      return 0
    fi
  elif command -v netstat >/dev/null 2>&1; then
    if netstat -tln | grep -q ":$port "; then
      return 0
    fi
  fi
  return 1
}

FRONTEND_PORT="${FRONTEND_PORT:-5174}"
if check_port "$FRONTEND_PORT"; then
  echo "Warning: port $FRONTEND_PORT appears to be in use."
  echo "You can set FRONTEND_PORT to another value or stop the other server."
  echo "Skipping frontend startup."
else
  start_frontend
fi

echo "Quick start script finished."

echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5174"
