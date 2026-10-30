import pytest
import os
from io import BytesIO
from app import db
from app.models import File, AuditLog


def test_dashboard_requires_login(client):
    """Test that dashboard requires authentication."""
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Please log in' in response.data


def test_dashboard_accessible(logged_in_client):
    """Test that dashboard is accessible when logged in."""
    response = logged_in_client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_upload_file_success(logged_in_client, app):
    """Test successful file upload."""
    data = {
        'file': (BytesIO(b'test file content'), 'test.txt'),
        'description': 'Test file description'
    }
    
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'File uploaded successfully' in response.data
    
    with app.app_context():
        file = File.query.filter_by(original_filename='test.txt').first()
        assert file is not None
        assert file.description == 'Test file description'
        assert file.uploader_id is not None


def test_upload_file_invalid_type(logged_in_client):
    """Test upload with invalid file type."""
    data = {
        'file': (BytesIO(b'malicious content'), 'malicious.exe'),
        'description': 'Test'
    }
    
    response = logged_in_client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    
    assert b'Invalid file type' in response.data


def test_upload_file_no_file(logged_in_client):
    """Test upload without file."""
    response = logged_in_client.post('/upload', data={}, content_type='multipart/form-data', follow_redirects=True)
    
    assert response.status_code == 200


def test_view_file_accessible_by_owner(logged_in_client, app, init_db):
    """Test that owner can view their file."""
    # Create a test file
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        test_file = File(
            filename='test_file.txt',
            original_filename='test.txt',
            file_path='/tmp/test.txt',
            file_size=100,
            uploader_id=user.id
        )
        db.session.add(test_file)
        db.session.commit()
        file_id = test_file.id
    
    response = logged_in_client.get(f'/file/{file_id}')
    assert response.status_code == 200
    assert b'test.txt' in response.data


def test_view_file_not_accessible_by_non_owner(logged_in_client, admin_client, app, init_db):
    """Test that non-owner cannot view file."""
    # Create a file as admin
    with app.app_context():
        from app.models import User
        admin = User.query.filter_by(username='admin').first()
        test_file = File(
            filename='admin_file.txt',
            original_filename='admin.txt',
            file_path='/tmp/admin.txt',
            file_size=100,
            uploader_id=admin.id
        )
        db.session.add(test_file)
        db.session.commit()
        file_id = test_file.id
    
    # Try to access as regular user
    response = logged_in_client.get(f'/file/{file_id}', follow_redirects=True)
    assert b'permission' in response.data.lower()


def test_download_file_accessible_by_owner(logged_in_client, app, init_db):
    """Test that owner can download their file."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_file.write(b'test content')
        temp_file.close()
        
        test_file = File(
            filename='test_file.txt',
            original_filename='test.txt',
            file_path=temp_file.name,
            file_size=12,
            uploader_id=user.id
        )
        db.session.add(test_file)
        db.session.commit()
        file_id = test_file.id
    
    response = logged_in_client.get(f'/download/{file_id}')
    assert response.status_code == 200
    
    # Cleanup
    os.unlink(temp_file.name)


def test_download_file_not_accessible_by_non_owner(logged_in_client, admin_client, app, init_db):
    """Test that non-owner cannot download file."""
    with app.app_context():
        from app.models import User
        admin = User.query.filter_by(username='admin').first()
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_file.write(b'admin content')
        temp_file.close()
        
        test_file = File(
            filename='admin_file.txt',
            original_filename='admin.txt',
            file_path=temp_file.name,
            file_size=12,
            uploader_id=admin.id
        )
        db.session.add(test_file)
        db.session.commit()
        file_id = test_file.id
    
    response = logged_in_client.get(f'/download/{file_id}', follow_redirects=True)
    assert b'permission' in response.data.lower()
    
    # Cleanup
    os.unlink(temp_file.name)


def test_delete_file_by_owner(logged_in_client, app, init_db):
    """Test that owner can delete their file."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_file.write(b'test content')
        temp_file.close()
        
        test_file = File(
            filename='test_file.txt',
            original_filename='test.txt',
            file_path=temp_file.name,
            file_size=12,
            uploader_id=user.id
        )
        db.session.add(test_file)
        db.session.commit()
        file_id = test_file.id
    
    response = logged_in_client.post(f'/delete/{file_id}', follow_redirects=True)
    assert b'File deleted successfully' in response.data
    
    with app.app_context():
        file = File.query.get(file_id)
        assert file is None
    
    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


def test_delete_file_not_by_owner(logged_in_client, admin_client, app, init_db):
    """Test that non-owner cannot delete file."""
    with app.app_context():
        from app.models import User
        admin = User.query.filter_by(username='admin').first()
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_file.write(b'admin content')
        temp_file.close()
        
        test_file = File(
            filename='admin_file.txt',
            original_filename='admin.txt',
            file_path=temp_file.name,
            file_size=12,
            uploader_id=admin.id
        )
        db.session.add(test_file)
        db.session.commit()
        file_id = test_file.id
    
    response = logged_in_client.post(f'/delete/{file_id}', follow_redirects=True)
    assert b'Only the file owner' in response.data
    
    with app.app_context():
        file = File.query.get(file_id)
        assert file is not None
    
    # Cleanup
    os.unlink(temp_file.name)


def test_audit_log_on_upload(logged_in_client, app):
    """Test that upload is logged."""
    data = {
        'file': (BytesIO(b'test content'), 'test.txt'),
        'description': 'Test'
    }
    
    logged_in_client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    
    with app.app_context():
        log = AuditLog.query.filter_by(action='upload').first()
        assert log is not None
        assert 'test.txt' in log.details
