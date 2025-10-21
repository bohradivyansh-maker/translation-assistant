@echo off
REM ========================================================================
REM Git Repository Setup and GitHub Upload Script
REM Automates the process of uploading your project to GitHub
REM ========================================================================

echo.
echo ========================================================================
echo    TRANSLATION ASSISTANT - GITHUB UPLOAD SCRIPT
echo ========================================================================
echo.
echo This script will help you upload your project to GitHub.
echo.
echo Prerequisites:
echo   1. Git must be installed (download from https://git-scm.com)
echo   2. You must have a GitHub account
echo   3. You must create a repository on GitHub first
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Git is not installed!
    echo Please download and install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo.
echo [Step 1/7] Checking Git configuration...

REM Check if user name is configured
git config user.name >nul 2>&1
if errorlevel 1 (
    echo.
    echo Git user name not configured.
    set /p gitname="Enter your name: "
    git config user.name "!gitname!"
)

REM Check if user email is configured
git config user.email >nul 2>&1
if errorlevel 1 (
    echo.
    echo Git user email not configured.
    set /p gitemail="Enter your email: "
    git config user.email "!gitemail!"
)

echo Git configuration:
git config user.name
git config user.email

echo.
echo [Step 2/7] Initializing Git repository...

REM Initialize Git if not already done
if not exist ".git" (
    git init
    echo Git repository initialized!
) else (
    echo Git repository already exists.
)

echo.
echo [Step 3/7] Cleaning up unnecessary files...

REM Remove files that shouldn't be in Git
if exist "venv" (
    echo Removing virtual environment folder...
    REM Don't actually delete, just note it
    echo   Note: venv/ will be ignored by .gitignore
)

if exist "*.log" (
    echo Removing log files...
    del /q *.log 2>nul
)

if exist "translation_memory.db" (
    echo Removing database file...
    del /q translation_memory.db 2>nul
)

if exist "build" (
    echo Removing build folder...
    rmdir /s /q build 2>nul
)

if exist "dist" (
    echo Removing dist folder...
    rmdir /s /q dist 2>nul
)

echo Cleanup complete!

echo.
echo [Step 4/7] Staging files for commit...

REM Add all files (respecting .gitignore)
git add .

echo Files staged. Let's see what will be committed:
git status --short

echo.
echo [Step 5/7] Creating commit...

set /p commit_msg="Enter commit message (or press Enter for default): "

if "%commit_msg%"=="" (
    set commit_msg=Initial commit: Context-Aware Translation Assistant NLP Project
)

git commit -m "%commit_msg%"

if errorlevel 1 (
    echo.
    echo ERROR: Commit failed! Check the error messages above.
    pause
    exit /b 1
)

echo Commit created successfully!

echo.
echo [Step 6/7] Adding GitHub remote...
echo.
echo Please go to GitHub and create a new repository:
echo   1. Visit: https://github.com/new
echo   2. Repository name: translation-assistant
echo   3. Description: Context-aware translation assistant using NLP
echo   4. Make it Public
echo   5. Do NOT initialize with README
echo   6. Click "Create repository"
echo.
pause

set /p github_url="Enter your GitHub repository URL (e.g., https://github.com/username/translation-assistant.git): "

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin %github_url%
    echo Remote added!
) else (
    echo Remote already exists. Updating...
    git remote set-url origin %github_url%
)

echo.
echo [Step 7/7] Pushing to GitHub...

REM Create main branch
git branch -M main

REM Push to GitHub
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed!
    echo.
    echo Common fixes:
    echo   1. Make sure the repository URL is correct
    echo   2. Check your internet connection
    echo   3. Verify you have permissions for this repository
    echo   4. Try: git push -u origin main --force (if you're sure)
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo    SUCCESS! Project uploaded to GitHub!
echo ========================================================================
echo.
echo Your repository is now available at:
echo %github_url://.git=%
echo.
echo Next steps:
echo   1. Visit your GitHub repository
echo   2. Add topics/tags (nlp, python, translation, etc.)
echo   3. Add a description
echo   4. Verify all files are uploaded
echo   5. Share the link with your professor!
echo.
echo To make future updates:
echo   git add .
echo   git commit -m "Your message"
echo   git push
echo.
echo ========================================================================

echo.
echo Press any key to open your repository in browser...
pause >nul

start "" "%github_url://.git=%"

echo.
echo Press any key to exit...
pause >nul
