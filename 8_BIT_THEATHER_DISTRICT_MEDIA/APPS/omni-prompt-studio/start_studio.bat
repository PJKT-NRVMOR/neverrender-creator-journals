@echo off
echo STARTING OMNI PROMPT STUDIO...
echo Please wait while the servers spin up...

cd /d "%~dp0"

:: Start the Express Backend
start "Omni Backend API" cmd /k "node server.js"

:: Start the React Frontend
cd frontend
start "Omni Frontend UI" cmd /k "npm run dev"

:: Wait for Vite to compile and start, then launch browser
timeout /t 5 /nobreak >nul
start http://localhost:5173
