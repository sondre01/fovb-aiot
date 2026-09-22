@echo off
title FOVB-AIoT Health Kiosk & Web Portal
cd /d "%~dp0"
echo ======================================================================
echo    FOVB-AIoT: 4-in-1 Vital Sign Sensors & AI Health Prediction
echo    Rizal Technological University - Pasig Campus Clinic Portal
echo ======================================================================
echo.
echo Starting Flask web server...
echo Access in your browser at: http://127.0.0.1:5000
echo.
echo Opening browser automatically in 2 seconds...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000
echo.
echo Press Ctrl + C to stop the server anytime.
echo.
python app.py
pause
