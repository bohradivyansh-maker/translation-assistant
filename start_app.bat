@echo off
REM Start Translation Assistant with Hotkey Fix
echo ============================================================
echo   Context-Aware Translation Assistant
echo   WITH HOTKEY FIX FOR Ctrl+Shift+T
echo ============================================================
echo.

cd /d "d:\Sem 7\NLP\Nlp Project\translation-assistant"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting application...
echo.
echo ============================================================
echo   HOW TO USE:
echo ============================================================
echo   1. Keep this window OPEN
echo   2. Go to any app (browser, notepad, Word)
echo   3. Select/highlight text
echo   4. Press Ctrl+Shift+T
echo   5. A popup will appear with translation
echo.
echo   Press Ctrl+C in THIS window to stop the app
echo ============================================================
echo.

python main.py --lang es

echo.
echo ============================================================
echo   App stopped. Press any key to close this window.
echo ============================================================
pause
