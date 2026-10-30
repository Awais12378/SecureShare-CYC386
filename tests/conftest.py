import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, File, FileShare, AuditLog


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    
    with app.app_context():
        db.create_all()
        
    yield app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    import shutil
    shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test runner for CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def init_db(app):
    """Initialize database with test data."""
    with app.app_context():
        # Create test users
        user1 = User(username='testuser', email='test@example.com')
        user1.set_password('TestPassword123!')
        user2 = User(username='otheruser', email='other@example.com')
        user2.set_password('OtherPassword123!')
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('AdminPassword123!')
        
        db.session.add_all([user1, user2, admin])
        db.session.commit()
        
        yield {'user1': user1, 'user2': user2, 'admin': admin}
        
        # Cleanup
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture
def auth_headers(client, init_db):
    """Get authentication headers for test user."""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'TestPassword123!'
    }, follow_redirects=True)
    
    # Return the client with session
    return client


@pytest.fixture
def logged_in_client(client, init_db):
    """Return a client with logged in user session."""
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'TestPassword123!'
    })
    return client


@pytest.fixture
def admin_client(client, init_db):
    """Return a client with logged in admin session."""
    client.post('/auth/login', data={
        'username': 'admin',
        'password': 'AdminPassword123!'
    })
    return client
