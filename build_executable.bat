@echo off
REM ========================================================================
REM Translation Assistant - Standalone Executable Builder
REM Creates a single .exe file that works without Python installation
REM ========================================================================

echo.
echo ========================================================================
echo    TRANSLATION ASSISTANT - EXECUTABLE BUILDER
echo ========================================================================
echo.
echo This script will create a standalone .exe file that can run on
echo any Windows PC without requiring Python installation.
echo.
echo NOTE: This process will take 10-20 minutes and create a large file
echo       ^(approximately 200-300 MB^)
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to create the virtual environment
    pause
    exit /b 1
)

echo.
echo [Step 1/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [Step 2/6] Installing PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo [Step 3/6] Cleaning up old build files...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec

echo [Step 4/6] Building standalone executable...
echo    This may take 10-20 minutes, please be patient...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "TranslationAssistant" ^
    --add-data "data;data" ^
    --hidden-import=deep_translator ^
    --hidden-import=deep_translator.google ^
    --hidden-import=spacy ^
    --hidden-import=nltk ^
    --hidden-import=nltk.data ^
    --hidden-import=pynput ^
    --hidden-import=pynput.keyboard ^
    --hidden-import=pynput.mouse ^
    --hidden-import=sklearn ^
    --hidden-import=gtts ^
    --hidden-import=playsound3 ^
    --collect-all deep_translator ^
    --collect-data spacy ^
    --collect-data nltk ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo [Step 5/6] Creating portable package...
if exist "portable_executable" rmdir /s /q portable_executable
mkdir portable_executable
mkdir portable_executable\data

copy /Y dist\TranslationAssistant.exe portable_executable\ >nul
xcopy /E /I /Y data portable_executable\data >nul
copy /Y README.md portable_executable\ 2>nul

REM Create a simple readme for the executable
(
echo ========================================================================
echo    TRANSLATION ASSISTANT - STANDALONE VERSION
echo ========================================================================
echo.
echo HOW TO USE:
echo -----------
echo 1. Double-click "TranslationAssistant.exe" to run
echo    ^(No Python installation required!^)
echo.
echo 2. Select any text in any application
echo.
echo 3. Press: Ctrl+Shift+T
echo.
echo 4. Choose your target language
echo.
echo 5. View translation instantly!
echo.
echo.
echo FIRST RUN:
echo ----------
echo • The first run may take 30-60 seconds to initialize
echo • Language models will be downloaded automatically
echo • Subsequent runs will be much faster
echo.
echo.
echo KEYBOARD SHORTCUTS:
echo ------------------
echo • Ctrl+Shift+T  - Trigger translation
echo • ESC          - Cancel or use default English
echo • Enter        - Confirm selection
echo.
echo.
echo SUPPORTED LANGUAGES:
echo -------------------
echo Spanish, French, German, Hindi, Japanese, Chinese, Arabic,
echo Portuguese, Russian, Italian, Korean, Turkish, Dutch, Polish, Vietnamese
echo.
echo.
echo TROUBLESHOOTING:
echo ---------------
echo • If Windows Defender blocks the app:
echo   1. Click "More info"
echo   2. Click "Run anyway"
echo   ^(This is normal for unsigned executables^)
echo.
echo • App not responding?
echo   - Close and restart TranslationAssistant.exe
echo.
echo • Hotkey not working?
echo   - Make sure the app is running ^(check Task Manager^)
echo   - Another program might be using Ctrl+Shift+T
echo.
echo • Antivirus warning?
echo   - Add exception for TranslationAssistant.exe
echo   - This is a false positive, the app is safe
echo.
echo.
echo SYSTEM REQUIREMENTS:
echo -------------------
echo • Windows 7/8/10/11 ^(64-bit recommended^)
echo • Internet connection ^(for translations^)
echo • 500MB free disk space
echo • NO Python installation required!
echo.
echo ========================================================================
) > portable_executable\README_STANDALONE.txt

echo [Step 6/6] Creating compressed package...

REM Get file size
for %%A in ("dist\TranslationAssistant.exe") do set filesize=%%~zA

echo.
echo Creating: TranslationAssistant-Standalone.zip
powershell -Command "Compress-Archive -Path 'portable_executable\*' -DestinationPath 'TranslationAssistant-Standalone.zip' -Force"

if exist "TranslationAssistant-Standalone.zip" (
    echo.
    echo ========================================================================
    echo    SUCCESS! Standalone executable created!
    echo ========================================================================
    echo.
    echo Package: TranslationAssistant-Standalone.zip
    echo Executable size: %filesize% bytes
    echo.
    echo WHAT'S INCLUDED:
    echo   - TranslationAssistant.exe ^(standalone, no Python needed^)
    echo   - data\ folder ^(configuration files^)
    echo   - README_STANDALONE.txt ^(user guide^)
    echo.
    echo HOW TO DISTRIBUTE:
    echo -----------------
    echo 1. Share TranslationAssistant-Standalone.zip via:
    echo    • USB drive
    echo    • Cloud storage ^(Google Drive, OneDrive, etc.^)
    echo    • File sharing service ^(WeTransfer, etc.^)
    echo.
    echo 2. Recipient instructions:
    echo    • Extract the .zip file
    echo    • Double-click TranslationAssistant.exe
    echo    • That's it! No installation needed!
    echo.
    echo NOTES:
    echo ------
    echo • Windows may show a security warning ^(normal for unsigned apps^)
    echo • Click "More info" then "Run anyway"
    echo • First run may take 30-60 seconds to initialize
    echo • Works on ANY Windows PC without Python!
    echo.
    echo ========================================================================
) else (
    echo.
    echo ERROR: Failed to create zip package!
    echo The executable is in: portable_executable\TranslationAssistant.exe
)

echo.
echo Press any key to open the package folder...
pause >nul
explorer "portable_executable"

echo.
echo Press any key to exit...
pause >nul
