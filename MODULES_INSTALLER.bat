@echo off
echo ================================
echo Installing Python requirements
echo ================================

REM Use python from PATH
python -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo ERROR: Python not found in PATH
    echo Please install Python and check "Add to PATH"
    pause
    exit /b 1
)

echo.
echo Installing requirements.txt...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo Requirements installed successfully!
pause