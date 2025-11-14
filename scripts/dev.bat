@echo off
REM Windows development script

echo ================================
echo NHL Simulation Game - Dev Mode
echo ================================
echo.

cd intelligence-service
call venv\Scripts\activate
python src\main.py

