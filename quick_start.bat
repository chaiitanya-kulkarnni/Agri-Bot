@echo off
cls
echo ================================================
echo  Grape Disease Detection - SUPER SIMPLE START
echo ================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo     Python found!

echo.
echo [2/3] Installing/Updating packages...
echo     This may take 5-10 minutes the first time...
python -m pip install --upgrade pip --quiet
python -m pip install Flask Werkzeug Pillow opencv-python pandas numpy scikit-learn requests --quiet
echo     Basic packages installed!

echo.
echo [3/3] Starting Flask server...
echo.
echo ================================================
echo  SERVER STARTING
echo  Open your browser and go to:
echo  
echo  http://localhost:5000
echo  
echo  Press Ctrl+C to stop the server
echo ================================================
echo.

python main.py

pause
