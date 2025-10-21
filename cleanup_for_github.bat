@echo off
REM ========================================================================
REM Clean Project for GitHub Upload
REM Removes unnecessary files before Git commit
REM ========================================================================

echo.
echo ========================================================================
echo    CLEANING PROJECT FOR GITHUB UPLOAD
echo ========================================================================
echo.

echo [1/5] Removing virtual environment folder...
if exist "venv" (
    echo   venv/ folder found - will be excluded by .gitignore
) else (
    echo   venv/ folder not found
)

echo.
echo [2/5] Removing Python cache files...
for /d /r %%d in (__pycache__) do (
    if exist "%%d" (
        echo   Removing: %%d
        rmdir /s /q "%%d" 2>nul
    )
)

echo.
echo [3/5] Removing log files...
if exist "*.log" (
    del /q *.log 2>nul
    echo   Removed *.log files
) else (
    echo   No log files found
)

echo.
echo [4/5] Removing database files...
if exist "translation_memory.db" (
    del /q translation_memory.db 2>nul
    echo   Removed translation_memory.db
) else (
    echo   No database file found
)

echo.
echo [5/5] Removing build artifacts...
if exist "build" (
    rmdir /s /q build 2>nul
    echo   Removed build/
)
if exist "dist" (
    rmdir /s /q dist 2>nul
    echo   Removed dist/
)
if exist "portable_executable" (
    rmdir /s /q portable_executable 2>nul
    echo   Removed portable_executable/
)
if exist "portable_package" (
    rmdir /s /q portable_package 2>nul
    echo   Removed portable_package/
)
if exist "*.zip" (
    del /q *.zip 2>nul
    echo   Removed *.zip files
)

echo.
echo ========================================================================
echo    CLEANUP COMPLETE!
echo ========================================================================
echo.
echo Files removed:
echo   - __pycache__/ folders
echo   - *.log files
echo   - translation_memory.db
echo   - build/ and dist/ folders
echo   - portable packages
echo.
echo Files kept (important for Git):
echo   - All source code (src/)
echo   - All documentation (*.md)
echo   - All scripts (*.bat)
echo   - requirements.txt
echo   - .gitignore
echo   - LICENSE
echo   - data/custom_dictionary.json
echo   - tests/
echo.
echo Note: venv/ folder will be automatically excluded by .gitignore
echo.
echo Next step: Run upload_to_github.bat to upload to GitHub
echo.
pause
