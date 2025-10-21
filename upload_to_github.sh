#!/bin/bash
# ========================================================================
# TRANSLATION ASSISTANT - GITHUB UPLOAD SCRIPT (BASH VERSION)
# For Git Bash (MINGW64) on Windows
# ========================================================================

echo ""
echo "========================================================================"
echo "   TRANSLATION ASSISTANT - GITHUB UPLOAD SCRIPT"
echo "========================================================================"
echo ""
echo "This script will help you upload your project to GitHub."
echo ""
echo "Prerequisites:"
echo "  1. Git is installed (you're using Git Bash, so you have it!)"
echo "  2. You have a GitHub account"
echo "  3. You need to create a repository on GitHub first"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# ========================================================================
# Step 1: Check if Git is configured
# ========================================================================
echo ""
echo "========================================================================"
echo "   STEP 1: GIT CONFIGURATION"
echo "========================================================================"
echo ""

GIT_USER=$(git config --global user.name)
GIT_EMAIL=$(git config --global user.email)

if [ -z "$GIT_USER" ]; then
    echo "Git username not configured."
    read -p "Enter your GitHub username: " username
    git config --global user.name "$username"
    echo "✓ Git username set to: $username"
else
    echo "✓ Git username: $GIT_USER"
fi

echo ""

if [ -z "$GIT_EMAIL" ]; then
    echo "Git email not configured."
    read -p "Enter your GitHub email: " email
    git config --global user.email "$email"
    echo "✓ Git email set to: $email"
else
    echo "✓ Git email: $GIT_EMAIL"
fi

# ========================================================================
# Step 2: Initialize Git Repository
# ========================================================================
echo ""
echo "========================================================================"
echo "   STEP 2: INITIALIZE GIT REPOSITORY"
echo "========================================================================"
echo ""

if [ -d ".git" ]; then
    echo "✓ Git repository already initialized"
    read -p "Do you want to reinitialize? (y/N): " reinit
    if [[ $reinit == "y" || $reinit == "Y" ]]; then
        rm -rf .git
        git init
        echo "✓ Repository reinitialized"
    fi
else
    git init
    echo "✓ Git repository initialized"
fi

# ========================================================================
# Step 3: Create/Verify .gitignore
# ========================================================================
echo ""
echo "========================================================================"
echo "   STEP 3: VERIFY .gitignore"
echo "========================================================================"
echo ""

if [ -f ".gitignore" ]; then
    echo "✓ .gitignore file exists"
    echo ""
    echo "Files that will be excluded:"
    echo "  - venv/"
    echo "  - __pycache__/"
    echo "  - *.log"
    echo "  - *.db"
    echo "  - build/ and dist/"
    echo "  - *.zip files"
else
    echo "WARNING: .gitignore file not found!"
fi

# ========================================================================
# Step 4: Stage Files
# ========================================================================
echo ""
echo "========================================================================"
echo "   STEP 4: STAGING FILES FOR COMMIT"
echo "========================================================================"
echo ""

echo "Adding all project files (excluding items in .gitignore)..."
git add .

echo ""
echo "Files to be committed:"
git status --short
echo ""

file_count=$(git status --short | wc -l)
echo "✓ Total files staged: $file_count"

# ========================================================================
# Step 5: Create Initial Commit
# ========================================================================
echo ""
echo "========================================================================"
echo "   STEP 5: CREATE INITIAL COMMIT"
echo "========================================================================"
echo ""

read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit - Context-Aware Translation Assistant"
fi

git commit -m "$commit_msg"

if [ $? -eq 0 ]; then
    echo "✓ Initial commit created successfully"
else
    echo "✗ Commit failed. Please check for errors above."
    exit 1
fi

# ========================================================================
# Step 6: Create GitHub Repository and Add Remote
# ========================================================================
echo ""
echo "========================================================================"
echo "   STEP 6: CONNECT TO GITHUB REPOSITORY"
echo "========================================================================"
echo ""
echo "IMPORTANT: Before continuing, create a repository on GitHub:"
echo ""
echo "  1. Go to: https://github.com/new"
echo "  2. Repository name: translation-assistant"
echo "  3. Description: Context-Aware Translation Assistant - NLP Project"
echo "  4. Make it PUBLIC (for academic submission)"
echo "  5. DO NOT initialize with README, .gitignore, or license"
echo "  6. Click 'Create repository'"
echo ""
read -p "Press Enter once you've created the repository on GitHub..."

echo ""
read -p "Enter your GitHub username: " gh_user
repo_url="https://github.com/$gh_user/translation-assistant.git"

echo ""
echo "Repository URL: $repo_url"
read -p "Is this correct? (Y/n): " confirm
if [[ $confirm == "n" || $confirm == "N" ]]; then
    read -p "Enter the full repository URL: " repo_url
fi

# Check if remote already exists
if git remote get-url origin &>/dev/null; then
    echo "Remote 'origin' already exists. Updating..."
    git remote set-url origin "$repo_url"
else
    git remote add origin "$repo_url"
fi

echo "✓ Remote repository configured: $repo_url"

# ========================================================================
# Step 7: Push to GitHub
# ========================================================================
echo ""
echo "========================================================================"
echo "   STEP 7: PUSH TO GITHUB"
echo "========================================================================"
echo ""

echo "Renaming branch to 'main'..."
git branch -M main

echo ""
echo "Pushing to GitHub..."
echo "NOTE: You may be prompted to enter your GitHub credentials."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================================"
    echo "   ✓ SUCCESS! PROJECT UPLOADED TO GITHUB"
    echo "========================================================================"
    echo ""
    echo "Your repository is now available at:"
    echo "  → $repo_url"
    echo ""
    echo "Next steps:"
    echo "  1. Visit your repository and add topics/tags:"
    echo "     - nlp, python, translation, spacy, nltk, machine-learning"
    echo ""
    echo "  2. Add a description on GitHub:"
    echo "     'Context-Aware Translation Assistant using NLP techniques'"
    echo ""
    echo "  3. Submit the repository link to your professor"
    echo ""
    echo "  4. Consider adding screenshots to your README.md"
    echo ""
    echo "Opening repository in browser..."
    start "https://github.com/$gh_user/translation-assistant" 2>/dev/null || \
    explorer "https://github.com/$gh_user/translation-assistant" 2>/dev/null || \
    echo "Please manually open: https://github.com/$gh_user/translation-assistant"
else
    echo ""
    echo "========================================================================"
    echo "   ✗ PUSH FAILED"
    echo "========================================================================"
    echo ""
    echo "Common issues:"
    echo "  1. Authentication failed - You may need to use a Personal Access Token"
    echo "  2. Repository doesn't exist - Make sure you created it on GitHub"
    echo "  3. Network issues - Check your internet connection"
    echo ""
    echo "To fix authentication issues:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Generate a new token (classic)"
    echo "  3. Use the token as your password when prompted"
    echo ""
    echo "Try pushing manually with:"
    echo "  git push -u origin main"
fi

echo ""
read -p "Press Enter to exit..."
