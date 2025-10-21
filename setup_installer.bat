@echo off
REM ========================================================================
REM Translation Assistant - Automated Installer for Distribution
REM This script prepares a portable package for other devices
REM ========================================================================

echo.
echo ========================================================================
echo    TRANSLATION ASSISTANT - PORTABLE PACKAGE CREATOR
echo ========================================================================
echo.
echo This script will create a portable package that can be easily
echo installed on other Windows PCs.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please make sure Python 3.11+ is installed and in PATH
    pause
    exit /b 1
)

echo.
echo [Step 1/5] Cleaning up old build files...
if exist "portable_package" rmdir /s /q portable_package
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

echo [Step 2/5] Creating portable package directory...
mkdir portable_package
mkdir portable_package\translation-assistant

echo [Step 3/5] Copying essential files...
xcopy /E /I /Y src portable_package\translation-assistant\src >nul
xcopy /E /I /Y data portable_package\translation-assistant\data >nul
copy /Y main.py portable_package\translation-assistant\ >nul
copy /Y config.py portable_package\translation-assistant\ >nul
copy /Y requirements.txt portable_package\translation-assistant\ >nul
copy /Y setup.bat portable_package\translation-assistant\ >nul
copy /Y start_app.bat portable_package\translation-assistant\ >nul
copy /Y README.md portable_package\translation-assistant\ >nul
copy /Y DEPLOYMENT_GUIDE.md portable_package\translation-assistant\ >nul
copy /Y LICENSE portable_package\translation-assistant\ 2>nul

echo [Step 4/5] Creating user-friendly quick start guide...
(
echo ========================================================================
echo    TRANSLATION ASSISTANT - QUICK START GUIDE
echo ========================================================================
echo.
echo FIRST-TIME SETUP:
echo -----------------
echo 1. Make sure Python 3.11+ is installed on your PC
echo    Download from: https://www.python.org/downloads/
echo    IMPORTANT: Check "Add Python to PATH" during installation
echo.
echo 2. Double-click "setup.bat" in the translation-assistant folder
echo    Wait 5-10 minutes for automatic installation
echo.
echo 3. Look for "Setup complete!" message
echo.
echo.
echo HOW TO USE:
echo -----------
echo 1. Double-click "start_app.bat" to run the translator
echo.
echo 2. Select any text in any application ^(browser, Word, etc.^)
echo.
echo 3. Press: Ctrl+Shift+T
echo.
echo 4. Choose your target language from the popup menu
echo.
echo 5. View the translation instantly!
echo.
echo.
echo SUPPORTED LANGUAGES:
echo -------------------
echo Spanish, French, German, Hindi, Japanese, Chinese, Arabic,
echo Portuguese, Russian, Italian, Korean, Turkish, Dutch, Polish, Vietnamese
echo.
echo.
echo KEYBOARD SHORTCUTS:
echo ------------------
echo • Ctrl+Shift+T  - Trigger translation
echo • ESC          - Cancel / Use default English
echo • Enter        - Confirm language selection
echo.
echo.
echo TROUBLESHOOTING:
echo ---------------
echo • App not responding?     → Restart start_app.bat
echo • Hotkey not working?     → Make sure app is running
echo • Installation errors?    → Run setup.bat as Administrator
echo • Translation errors?     → Check internet connection
echo • For detailed help       → Read DEPLOYMENT_GUIDE.md
echo.
echo.
echo SYSTEM REQUIREMENTS:
echo -------------------
echo • Windows 7/8/10/11 ^(64-bit recommended^)
echo • Python 3.11 or higher
echo • 2GB free disk space
echo • Internet connection ^(first-time setup only^)
echo.
echo.
echo NEED MORE HELP?
echo --------------
echo Read DEPLOYMENT_GUIDE.md for detailed instructions
echo Check logs in: translation-assistant\logs\translator.log
echo.
echo ========================================================================
) > portable_package\QUICK_START.txt

echo [Step 5/5] Creating compressed package...

REM Create timestamp for filename
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set timestamp=%mydate%_%mytime%

echo.
echo Creating: translation-assistant-portable_%timestamp%.zip
powershell -Command "Compress-Archive -Path 'portable_package\*' -DestinationPath 'translation-assistant-portable_%timestamp%.zip' -Force"

if exist "translation-assistant-portable_%timestamp%.zip" (
    echo.
    echo ========================================================================
    echo    SUCCESS! Portable package created!
    echo ========================================================================
    echo.
    echo Package location: translation-assistant-portable_%timestamp%.zip
    echo Package size: 
    for %%A in ("translation-assistant-portable_%timestamp%.zip") do echo    %%~zA bytes
    echo.
    echo This package contains:
    echo   - All source code
    echo   - Setup scripts
    echo   - Documentation
    echo   - Quick start guide
    echo.
    echo HOW TO DISTRIBUTE:
    echo -----------------
    echo 1. Share the .zip file via:
    echo    • USB drive
    echo    • Google Drive / OneDrive / Dropbox
    echo    • Email ^(if small enough^)
    echo    • WeTransfer ^(for larger files^)
    echo.
    echo 2. Recipient instructions:
    echo    • Extract the .zip file
    echo    • Read QUICK_START.txt
    echo    • Run setup.bat ^(one-time setup^)
    echo    • Run start_app.bat ^(to use app^)
    echo.
    echo ========================================================================
) else (
    echo.
    echo ERROR: Failed to create zip package!
    echo Try manually compressing the 'portable_package' folder
)

echo.
echo Press any key to open the package folder...
pause >nul
explorer "portable_package"

echo.
echo Press any key to exit...
pause >nul
