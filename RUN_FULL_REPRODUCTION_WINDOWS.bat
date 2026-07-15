@echo off
cd /d %~dp0
python run_full_reproduction.py
if errorlevel 1 exit /b %errorlevel%
pause
