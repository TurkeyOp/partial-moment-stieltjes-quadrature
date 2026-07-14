@echo off
title Partial-Moment Quadrature Reproduction

echo Installing required Python packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Installation failed.
    pause
    exit /b 1
)

echo.
echo Running the full reproduction workflow...
python run_all.py
if errorlevel 1 (
    echo.
    echo The project reported a failed test.
    pause
    exit /b 1
)

echo.
echo Project completed successfully.
pause
