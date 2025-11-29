#!/bin/bash

echo "========================================"
echo "  AI Dungeon Master - Quick Start"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "[ERROR] .env file not found!"
    echo ""
    echo "Please create a .env file with your API key."
    echo "Copy .env.example to .env and edit it."
    echo ""
    exit 1
fi

echo "Starting backend server..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 5

echo ""
echo "========================================"
echo "  Servers are starting!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Open http://localhost:3000 in your browser"
echo ""
echo "Press Ctrl+C to stop servers"
echo ""

# Wait for user interrupt
wait

