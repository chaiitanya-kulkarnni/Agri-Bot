@echo off
echo ================================================
echo  Grape Plant Disease Detection System
echo  Starting Application...
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check if database exists
if not exist "mydatabase.db" (
    echo.
    echo WARNING: Database file 'mydatabase.db' not found!
    echo Please create the database or run the app to auto-create it.
    echo.
)

REM Start the Flask application
echo.
echo ================================================
echo  Starting Flask Server...
echo  Access the app at: http://localhost:5000
echo  Press Ctrl+C to stop the server
echo ================================================
echo.
python main.py

pause
