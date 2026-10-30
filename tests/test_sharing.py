import pytest
from app import db
from app.models import File, FileShare, AuditLog


def test_share_file_by_owner(logged_in_client, app, init_db):
    """Test that owner can share file."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        other = User.query.filter_by(username='otheruser').first()
        
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
    
    response = logged_in_client.post(f'/share/{file_id}', data={
        'username': 'otheruser',
        'permission': 'read'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'shared with otheruser' in response.data.lower()
    
    with app.app_context():
        share = FileShare.query.filter_by(file_id=file_id, recipient_id=other.id).first()
        assert share is not None
        assert share.permission == 'read'


def test_share_file_not_by_owner(logged_in_client, admin_client, app, init_db):
    """Test that non-owner cannot share file."""
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
    
    response = logged_in_client.post(f'/share/{file_id}', data={
        'username': 'otheruser',
        'permission': 'read'
    }, follow_redirects=True)
    
    assert b'Only the file owner' in response.data


def test_share_file_with_nonexistent_user(logged_in_client, app, init_db):
    """Test sharing with nonexistent user."""
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
    
    response = logged_in_client.post(f'/share/{file_id}', data={
        'username': 'nonexistent',
        'permission': 'read'
    }, follow_redirects=True)
    
    assert b'User not found' in response.data


def test_share_file_with_self(logged_in_client, app, init_db):
    """Test sharing file with self."""
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
    
    response = logged_in_client.post(f'/share/{file_id}', data={
        'username': 'testuser',
        'permission': 'read'
    }, follow_redirects=True)
    
    assert b'cannot share a file with yourself' in response.data


def test_share_file_duplicate(logged_in_client, app, init_db):
    """Test sharing file that's already shared."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        other = User.query.filter_by(username='otheruser').first()
        
        test_file = File(
            filename='test_file.txt',
            original_filename='test.txt',
            file_path='/tmp/test.txt',
            file_size=100,
            uploader_id=user.id
        )
        db.session.add(test_file)
        db.session.commit()
        
        # Create existing share
        share = FileShare(
            file_id=test_file.id,
            recipient_id=other.id,
            shared_by_id=user.id,
            permission='read'
        )
        db.session.add(share)
        db.session.commit()
        file_id = test_file.id
    
    response = logged_in_client.post(f'/share/{file_id}', data={
        'username': 'otheruser',
        'permission': 'read'
    }, follow_redirects=True)
    
    assert b'already shared' in response.data


def test_revoke_share_by_owner(logged_in_client, app, init_db):
    """Test that owner can revoke share."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        other = User.query.filter_by(username='otheruser').first()
        
        test_file = File(
            filename='test_file.txt',
            original_filename='test.txt',
            file_path='/tmp/test.txt',
            file_size=100,
            uploader_id=user.id
        )
        db.session.add(test_file)
        db.session.commit()
        
        share = FileShare(
            file_id=test_file.id,
            recipient_id=other.id,
            shared_by_id=user.id,
            permission='read'
        )
        db.session.add(share)
        db.session.commit()
        share_id = share.id
    
    response = logged_in_client.get(f'/revoke/{share_id}', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Access revoked' in response.data
    
    with app.app_context():
        share = FileShare.query.get(share_id)
        assert share is None


def test_revoke_share_not_by_owner(logged_in_client, admin_client, app, init_db):
    """Test that non-owner cannot revoke share."""
    with app.app_context():
        from app.models import User
        admin = User.query.filter_by(username='admin').first()
        other = User.query.filter_by(username='otheruser').first()
        
        test_file = File(
            filename='admin_file.txt',
            original_filename='admin.txt',
            file_path='/tmp/admin.txt',
            file_size=100,
            uploader_id=admin.id
        )
        db.session.add(test_file)
        db.session.commit()
        
        share = FileShare(
            file_id=test_file.id,
            recipient_id=other.id,
            shared_by_id=admin.id,
            permission='read'
        )
        db.session.add(share)
        db.session.commit()
        share_id = share.id
    
    response = logged_in_client.get(f'/revoke/{share_id}', follow_redirects=True)
    
    assert b'Only the file owner' in response.data


def test_shared_file_accessible_by_recipient(logged_in_client, app, init_db):
    """Test that recipient can access shared file."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        other = User.query.filter_by(username='otheruser').first()
        
        test_file = File(
            filename='test_file.txt',
            original_filename='test.txt',
            file_path='/tmp/test.txt',
            file_size=100,
            uploader_id=user.id
        )
        db.session.add(test_file)
        db.session.commit()
        
        share = FileShare(
            file_id=test_file.id,
            recipient_id=other.id,
            shared_by_id=user.id,
            permission='read'
        )
        db.session.add(share)
        db.session.commit()
        file_id = test_file.id
    
    # Login as other user
    client = logged_in_client
    client.get('/auth/logout', follow_redirects=True)
    client.post('/auth/login', data={
        'username': 'otheruser',
        'password': 'OtherPassword123!'
    })
    
    response = client.get(f'/file/{file_id}')
    assert response.status_code == 200


def test_audit_log_on_share(logged_in_client, app, init_db):
    """Test that sharing is logged."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        other = User.query.filter_by(username='otheruser').first()
        
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
    
    logged_in_client.post(f'/share/{file_id}', data={
        'username': 'otheruser',
        'permission': 'read'
    }, follow_redirects=True)
    
    with app.app_context():
        log = AuditLog.query.filter_by(action='share').first()
        assert log is not None
        assert 'otheruser' in log.details


def test_audit_log_on_revoke(logged_in_client, app, init_db):
    """Test that revoking is logged."""
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(username='testuser').first()
        other = User.query.filter_by(username='otheruser').first()
        
        test_file = File(
            filename='test_file.txt',
            original_filename='test.txt',
            file_path='/tmp/test.txt',
            file_size=100,
            uploader_id=user.id
        )
        db.session.add(test_file)
        db.session.commit()
        
        share = FileShare(
            file_id=test_file.id,
            recipient_id=other.id,
            shared_by_id=user.id,
            permission='read'
        )
        db.session.add(share)
        db.session.commit()
        share_id = share.id
    
    logged_in_client.get(f'/revoke/{share_id}', follow_redirects=True)
    
    with app.app_context():
        log = AuditLog.query.filter_by(action='revoke').first()
        assert log is not None
        assert 'otheruser' in log.details
