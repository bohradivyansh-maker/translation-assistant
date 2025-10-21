# Contributing to Translation Assistant

Thank you for considering contributing to the Translation Assistant project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Log files if available

### Suggesting Enhancements

Feature requests are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Examples if applicable

### Pull Requests

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/YourFeature`)
3. **Commit** your changes (`git commit -m 'Add YourFeature'`)
4. **Push** to the branch (`git push origin feature/YourFeature`)
5. **Open** a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and small
- Write descriptive variable names

### Testing

- Test your changes thoroughly
- Add unit tests for new features
- Ensure existing tests pass
- Test on different systems if possible

### Documentation

- Update README.md for new features
- Add docstrings to new code
- Update USER_GUIDE.md if UI changes
- Include examples where helpful

## Development Setup

```powershell
# Clone your fork
git clone https://github.com/yourusername/translation-assistant.git
cd translation-assistant

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8

# Run tests
pytest tests/
```

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## Questions?

Feel free to open an issue for questions or join the discussion!

Thank you for contributing! 🙏
