@echo off
echo ========================================
echo   AI Dungeon Master - Quick Start
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo.
    echo Please create a .env file with your API key.
    echo Copy .env.example to .env and edit it.
    echo.
    pause
    exit /b 1
)

echo Starting backend server...
start "Backend Server" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting frontend server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   Servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Open http://localhost:3000 in your browser
echo.
echo Press any key to exit this window...
pause >nul

