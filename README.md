# SecureShare

A secure file sharing and collaboration platform built with security-first principles for the CYC386 Secure Software Design and Development course.

## Features

- **Secure Authentication**: Password hashing with PBKDF2, session management
- **Role-Based Access Control (RBAC)**: User and admin roles with appropriate permissions
- **Secure File Storage**: Files stored outside web root with secure access endpoints
- **File Sharing**: Share files with specific users, manage permissions, revoke access
- **Audit Logging**: Comprehensive logging of all security-relevant events
- **CSRF Protection**: All forms protected with CSRF tokens
- **Input Validation**: Server-side validation for file types and sizes
- **Responsive UI**: Clean, professional interface built with Bootstrap 5

## Tech Stack

- **Backend**: Python 3.12, Flask, SQLAlchemy, SQLite
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with CSRF protection
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Testing**: pytest, pytest-flask
- **Security**: OWASP best practices, secure defaults

## Project Structure

```
secureshare/
├── app/
│   ├── __init__.py           # App factory
│   ├── config.py             # Configuration classes
│   ├── models.py             # SQLAlchemy models
│   ├── auth/                 # Authentication blueprint
│   ├── main/                 # Main application blueprint
│   ├── admin/                # Admin blueprint
│   ├── templates/            # Jinja2 templates
│   └── static/               # CSS, JS, images
├── instance/                  # Instance data (uploads, SQLite DB)
│   ├── uploads/              # Uploaded files (outside web root)
│   └── secureshare.db        # SQLite database
├── tests/                    # pytest tests
├── scripts/                  # Utility scripts
│   └── seed_data.py          # Database seeding script
├── security_lab/             # Disabled security lab for demonstrations
├── native_module/            # C/GCC demonstration module
├── .github/workflows/        # CI/CD workflows
├── requirements.txt
├── .env.example
├── .gitignore
├── run.py                    # Application entry point
├── start.bat                 # Windows startup script
└── start.sh                  # Unix startup script
```

## Quick Start

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "SSD LAB MIDTERM"
```

2. Run the startup script (recommended):

**Windows:**
```cmd
start.bat
```

**Unix/Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

The script will:
- Create a virtual environment
- Install dependencies
- Initialize the database with seed data
- Start the application

3. Access the application at: http://127.0.0.1:5000

### Manual Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:

**Windows:**
```cmd
venv\Scripts\activate
```

**Unix/Linux/Mac:**
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python scripts/seed_data.py
```

5. Run the application:
```bash
python run.py
```

## Test Credentials

After running the seed script, you can use these test accounts:

- **Admin**: `admin` / `AdminPassword123!`
- **User 1**: `alice` / `AlicePassword123!`
- **User 2**: `bob` / `BobPassword123!`
- **User 3**: `charlie` / `CharliePassword123!`

## Running Tests

```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/Linux/Mac

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html
```

## Configuration

Configuration is managed through environment variables. Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key configuration options:
- `SECRET_KEY`: Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL`: Database connection string
- `UPLOAD_FOLDER`: Path to store uploaded files
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

## Security Features

### Authentication & Authorization
- PBKDF2 password hashing with SHA-256
- Secure session management with HTTP-only cookies
- Role-based access control (user/admin)
- Login attempt logging

### File Security
- Files stored outside web root (`instance/uploads/`)
- Secure random filenames to prevent collisions
- File type validation (whitelist approach)
- File size limits (16MB default)
- Authorization checks on all file operations

### Input Validation
- Server-side validation on all inputs
- CSRF protection on all forms
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via Jinja2 auto-escaping

### Audit Logging
- All security-relevant events logged
- Tracks: uploads, downloads, shares, revokes, logins, etc.
- Records: user, action, timestamp, IP address, user agent

### Secure Headers
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block

## API Endpoints

### Authentication
- `GET /` - Landing page
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### File Management
- `GET /dashboard` - User dashboard
- `GET /my-files` - List owned files
- `GET /shared-with-me` - List shared files
- `GET/POST /upload` - Upload file
- `GET /file/<id>` - View file details
- `GET /download/<id>` - Download file
- `GET/POST /share/<id>` - Share file
- `GET /revoke/<share_id>` - Revoke share
- `POST /delete/<id>` - Delete file

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - List all users
- `GET /admin/user/<id>` - View user details
- `POST /admin/user/<id>/toggle-admin` - Toggle admin status
- `POST /admin/user/<id>/delete` - Delete user
- `GET /admin/files` - List all files
- `GET /admin/audit-logs` - View audit logs

## Development

### Database Schema

The application uses SQLAlchemy ORM with the following models:

- **User**: User accounts with authentication and authorization
- **File**: Uploaded file metadata
- **FileShare**: File sharing relationships
- **AuditLog**: Security event logging

See `app/models.py` for detailed schema definitions.

### Adding New Features

1. Create a new blueprint in `app/`
2. Define routes in `routes.py`
3. Create forms in `forms.py`
4. Add templates in `templates/`
5. Register blueprint in `app/__init__.py`
6. Add tests in `tests/`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Security

See [SECURITY.md](SECURITY.md) for security policies and vulnerability reporting.

## License

This project is for educational purposes for the CYC386 Secure Software Design and Development course.

## Acknowledgments

- CYC386 Secure Software Design and Development course
- OWASP Secure Coding Practices
- Flask documentation and community
