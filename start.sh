#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "=========================================="
echo "🐍 Starting PyKtionary Full-Stack App..."
echo "=========================================="

# 1. Start Backend
echo "Starting FastAPI backend on http://127.0.0.1:8000..."
cd "$DIR/backend"
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment and installing dependencies..."
    python3 -m venv .venv
    ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python -m app.seed_data
    ./.venv/bin/python -m app.extractor
fi

./.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# 2. Start Frontend
echo "Starting Vite Frontend on http://127.0.0.1:5173..."
cd "$DIR/frontend"
if [ ! -d "node_modules" ]; then
    npm install
fi

npm run dev -- --host 127.0.0.1 --port 5173 &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit" SIGINT SIGTERM

echo ""
echo "✨ PyKtionary is live!"
echo "👉 Frontend: http://127.0.0.1:5173"
echo "👉 API Docs: http://127.0.0.1:8000/docs"
echo "Press Ctrl+C to terminate both servers."
wait
