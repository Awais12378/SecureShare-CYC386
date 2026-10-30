import pytest
from app.models import User, AuditLog


def test_register(client, app):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'NewPassword123!',
        'password2': 'NewPassword123!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'
        assert user.check_password('NewPassword123!')
        assert not user.is_admin


def test_register_duplicate_username(client, init_db):
    """Test registration with duplicate username."""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'Password123!',
        'password2': 'Password123!'
    }, follow_redirects=True)
    
    assert b'Username already taken' in response.data


def test_register_duplicate_email(client, init_db):
    """Test registration with duplicate email."""
    response = client.post('/auth/register', data={
        'username': 'different',
        'email': 'test@example.com',
        'password': 'Password123!',
        'password2': 'Password123!'
    }, follow_redirects=True)
    
    assert b'Email already registered' in response.data


def test_register_password_mismatch(client):
    """Test registration with password mismatch."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'Password123!',
        'password2': 'DifferentPassword123!'
    }, follow_redirects=True)
    
    assert b'Passwords must match' in response.data


def test_login_success(client, init_db):
    """Test successful login."""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'TestPassword123!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_login_invalid_username(client, init_db):
    """Test login with invalid username."""
    response = client.post('/auth/login', data={
        'username': 'nonexistent',
        'password': 'TestPassword123!'
    }, follow_redirects=True)
    
    assert b'Invalid username or password' in response.data


def test_login_invalid_password(client, init_db):
    """Test login with invalid password."""
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'WrongPassword123!'
    }, follow_redirects=True)
    
    assert b'Invalid username or password' in response.data


def test_logout(logged_in_client):
    """Test logout."""
    response = logged_in_client.get('/auth/logout', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'You have been logged out' in response.data
    assert b'Login' in response.data


def test_logout_requires_login(client):
    """Test that logout redirects when not logged in."""
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200


def test_audit_log_on_register(client, app):
    """Test that registration is logged."""
    client.post('/auth/register', data={
        'username': 'audituser',
        'email': 'audit@example.com',
        'password': 'Password123!',
        'password2': 'Password123!'
    }, follow_redirects=True)
    
    with app.app_context():
        log = AuditLog.query.filter_by(action='register').first()
        assert log is not None
        assert 'audituser' in log.details


def test_audit_log_on_login(client, app, init_db):
    """Test that login is logged."""
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'TestPassword123!'
    }, follow_redirects=True)
    
    with app.app_context():
        log = AuditLog.query.filter_by(action='login').first()
        assert log is not None
        assert 'testuser' in log.details


def test_audit_log_on_failed_login(client, app, init_db):
    """Test that failed login is logged."""
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'WrongPassword'
    }, follow_redirects=True)
    
    with app.app_context():
        log = AuditLog.query.filter_by(action='login_failed').first()
        assert log is not None
