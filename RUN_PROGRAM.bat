@echo off
echo ================================
echo Running python program...
echo ================================

REM Use python from PATH
python3 runVolGen.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to run the script
    pause
    exit /b 1
)

pause