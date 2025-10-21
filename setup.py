"""
Setup and Installation Script
Automates the installation process for Translation Assistant
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function"""
    print_header("Translation Assistant - Setup Script")
    
    # Check Python version
    print(f"\nPython Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ is required")
        sys.exit(1)
    print("✓ Python version OK")
    
    # Install requirements
    print_header("Installing Python Packages")
    if not run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    ):
        print("\n⚠ Warning: Some packages may have failed to install")
        print("   You may need to install them manually")
    
    # Download spaCy model
    print_header("Downloading spaCy Language Model")
    run_command(
        "python -m spacy download en_core_web_sm",
        "Downloading en_core_web_sm model"
    )
    
    # Download NLTK data
    print_header("Downloading NLTK Data")
    nltk_downloads = [
        'punkt',
        'stopwords',
        'wordnet',
        'averaged_perceptron_tagger',
        'omw-1.4'
    ]
    
    for data in nltk_downloads:
        run_command(
            f'python -c "import nltk; nltk.download(\'{data}\', quiet=True)"',
            f"Downloading NLTK {data}"
        )
    
    # Create data directory
    print_header("Creating Data Directory")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print(f"✓ Data directory created: {data_dir.absolute()}")
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    print(f"✓ Models directory created: {models_dir.absolute()}")
    
    # Verify installation
    print_header("Verifying Installation")
    
    checks = [
        ("import googletrans", "googletrans"),
        ("import spacy", "spacy"),
        ("import nltk", "nltk"),
        ("import pynput", "pynput"),
        ("import pyperclip", "pyperclip"),
        ("import gtts", "gTTS"),
        ("import tkinter", "tkinter"),
    ]
    
    failed = []
    for import_cmd, package_name in checks:
        try:
            exec(import_cmd)
            print(f"✓ {package_name} installed correctly")
        except ImportError:
            print(f"✗ {package_name} not found")
            failed.append(package_name)
    
    # Final summary
    print_header("Setup Complete")
    
    if failed:
        print(f"\n⚠ The following packages failed to install:")
        for pkg in failed:
            print(f"  - {pkg}")
        print("\nPlease install them manually:")
        print(f"  pip install {' '.join(failed)}")
    else:
        print("\n✓ All packages installed successfully!")
    
    print("\n" + "="*60)
    print("🚀 Ready to use!")
    print("="*60)
    print("\nTo start the application:")
    print("  python main.py --lang es")
    print("\nFor help:")
    print("  python main.py --help")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
