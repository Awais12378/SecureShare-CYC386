# Contributing to SecureShare

Thank you for your interest in contributing to SecureShare! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, constructive, and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- Basic knowledge of Flask, SQLAlchemy, and web security

### Setting Up Development Environment

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/secureshare.git
cd secureshare
```

3. Create a virtual environment:
```bash
python -m venv venv
```

4. Activate the virtual environment:

**Windows:**
```cmd
venv\Scripts\activate
```

**Unix/Linux/Mac:**
```bash
source venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Initialize the database:
```bash
python scripts/seed_data.py
```

7. Run the application:
```bash
python run.py
```

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/add-two-factor-auth`
- `fix/fix-file-upload-validation`
- `docs/update-readme`

### Making Changes

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following the code style guidelines

3. Write tests for your changes:
```bash
pytest tests/
```

4. Ensure all tests pass:
```bash
pytest -v
```

5. Commit your changes with descriptive messages:
```bash
git add .
git commit -m "Add feature: descriptive message"
```

6. Push to your fork:
```bash
git push origin feature/your-feature-name
```

7. Create a pull request

## Code Style Guidelines

### Python

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable and function names
- Add docstrings to functions and classes

### Example:

```python
def upload_file(user_id, file_data, description):
    """
    Upload a file for a specific user.

    Args:
        user_id (int): The ID of the user uploading the file
        file_data (FileStorage): The file data from the request
        description (str): Optional file description

    Returns:
        File: The created File object

    Raises:
        ValueError: If file type is not allowed
    """
    # Implementation
    pass
```

### HTML/Templates

- Use Bootstrap 5 components
- Follow consistent indentation
- Use semantic HTML
- Include appropriate accessibility attributes

### JavaScript

- Use modern ES6+ syntax
- Keep functions small and focused
- Add comments for complex logic

## Testing

### Writing Tests

- Write tests for all new features
- Write tests for bug fixes
- Aim for high code coverage
- Use descriptive test names

### Test Structure

```python
def test_feature_scenario():
    """Test description."""
    # Arrange
    setup_data()
    
    # Act
    result = perform_action()
    
    # Assert
    assert result == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run with verbose output
pytest -v
```

## Security Considerations

When contributing to SecureShare, keep security in mind:

1. **Never** expose secrets or credentials
2. **Always** validate user input
3. **Always** use parameterized queries (SQLAlchemy handles this)
4. **Always** check authorization before sensitive operations
5. **Never** trust client-side validation
6. **Always** log security-relevant events
7. **Never** store passwords in plain text

## Documentation

### Updating Documentation

- Keep README.md up to date
- Document new features
- Update SECURITY.md for security changes
- Add inline comments for complex code

### API Documentation

If adding new endpoints, document:
- Purpose
- Parameters
- Return values
- Authentication requirements
- Authorization requirements

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are descriptive
- [ ] No sensitive data included

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe tests performed

## Security Considerations
Any security implications

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No sensitive data
```

## Issue Reporting

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version)
- Screenshots if applicable

### Feature Requests

Include:
- Description of the feature
- Use case
- Proposed implementation (if known)
- Potential impact on existing features

## Questions

For questions about the project:
1. Check existing documentation
2. Search existing issues
3. Create a new issue with the "question" label

## Recognition

Contributors will be acknowledged in the project documentation.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Contact

For questions about contributing, contact the project maintainers.
