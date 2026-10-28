#!/bin/bash
# ==============================================================================
# TestPilot AI — One-Click Launch Script (PS-03)
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================================="
echo "  🚀 Starting TestPilot AI Platform (PS-03)"
echo "=========================================================="

# Check Python environment
if [ ! -d "backend/venv" ]; then
    echo "--> Creating Python virtual environment..."
    python3 -m venv backend/venv
    backend/venv/bin/pip install --upgrade pip
    backend/venv/bin/pip install -r backend/requirements.txt
    backend/venv/bin/playwright install chromium
fi

# Check frontend node_modules
if [ ! -d "frontend/node_modules" ]; then
    echo "--> Installing frontend dependencies..."
    npm --prefix frontend install
fi

echo "--> Starting Backend FastAPI Server on http://localhost:8000..."
backend/venv/bin/uvicorn backend.main:app --port 8000 --host 0.0.0.0 &
BACKEND_PID=$!

echo "--> Starting Frontend Vite Dev Server on http://localhost:5173..."
npm --prefix frontend run dev &
FRONTEND_PID=$!

cleanup() {
    echo ""
    echo "--> Shutting down TestPilot AI servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "--> TestPilot AI stopped cleanly. Goodbye!"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo ""
echo "=========================================================="
echo "  ✨ TestPilot AI is LIVE and Ready for Demonstration!"
echo "=========================================================="
echo "  • Dashboard Web UI:      http://localhost:5173"
echo "  • Backend API & Docs:    http://localhost:8000/docs"
echo "  • Built-in Target Shop:  http://localhost:8000/demo/shop"
echo "=========================================================="
echo "Press Ctrl+C to terminate both servers."
echo ""

wait
