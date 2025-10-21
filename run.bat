@echo off
REM Quick launcher for Translation Assistant

echo Starting Context-Aware Translation Assistant...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if language argument provided
if "%1"=="" (
    echo Using default language: Spanish
    python main.py --lang es
) else (
    echo Using language: %1
    python main.py --lang %1
)
