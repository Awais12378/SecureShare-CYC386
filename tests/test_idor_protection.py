"""
IDOR (Insecure Direct Object Reference) Protection Tests

PURPOSE: Verify that object-level authorization is properly implemented
         and that unauthorized access to resources is prevented.

CWE: CWE-639 (Authorization Bypass Through User-Controlled Key)
OWASP: A01:2021 - Broken Access Control

SCENARIO: Test that users cannot access files they don't own or haven't been shared with them,
         even if they can guess or enumerate file IDs.
"""

import pytest
from app import create_app, db
from app.models import User, File, FileShare, AuditLog
from flask_login import login_user, logout_user


class TestIDORProtection:
    """Test suite for IDOR protection in file access"""
    
    @pytest.fixture
    def app(self):
        """Create application with test database"""
        app = create_app('testing')
        app.config['TESTING'] = True
        
        with app.app_context():
            db.create_all()
        
        yield app
        
        with app.app_context():
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def user_a(self, app):
        """Create User A (file owner)"""
        with app.app_context():
            user_a = User(
                username='user_a',
                email='user_a@example.com',
                is_admin=False
            )
            user_a.set_password('UserAPassword123!')
            db.session.add(user_a)
            db.session.commit()
            # Store ID before expunging
            user_id = user_a.id
            username = user_a.username
            db.session.expunge(user_a)
            # Return a simple dict-like object with the needed data
            return type('SimpleUser', (), {'id': user_id, 'username': username})()
    
    @pytest.fixture
    def user_b(self, app):
        """Create User B (unauthorized user)"""
        with app.app_context():
            user_b = User(
                username='user_b',
                email='user_b@example.com',
                is_admin=False
            )
            user_b.set_password('UserBPassword123!')
            db.session.add(user_b)
            db.session.commit()
            db.session.expunge(user_b)  # Detach from session
            return user_b
    
    @pytest.fixture
    def admin_user(self, app):
        """Create admin user"""
        with app.app_context():
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('AdminPassword123!')
            db.session.add(admin)
            db.session.commit()
            db.session.expunge(admin)  # Detach from session
            return admin
    
    @pytest.fixture
    def user_a_file(self, app, user_a):
        """Create a file owned by User A"""
        with app.app_context():
            import tempfile
            import os
            
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_file.write(b'This is User A\'s confidential file.')
            temp_file.close()
            
            file = File(
                filename='user_a_confidential.txt',
                original_filename='confidential.txt',
                file_path=temp_file.name,
                file_size=45,
                content_type='text/plain',
                uploader_id=user_a.id,
                description='Confidential document for User A'
            )
            db.session.add(file)
            db.session.commit()
            db.session.expunge(file)  # Detach from session
            
            # Store temp file path for cleanup
            file._temp_path = temp_file.name
            
            return file
    
    @pytest.fixture
    def user_b_file(self, app, user_b):
        """Create a file owned by User B"""
        with app.app_context():
            import tempfile
            import os
            
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_file.write(b'This is User B\'s confidential file.')
            temp_file.close()
            
            file = File(
                filename='user_b_private.txt',
                original_filename='private.txt',
                file_path=temp_file.name,
                file_size=40,
                content_type='text/plain',
                uploader_id=user_b.id,
                description='Private document for User B'
            )
            db.session.add(file)
            db.session.commit()
            db.session.expunge(file)  # Detach from session
            
            # Store temp file path for cleanup
            file._temp_path = temp_file.name
            
            return file
    
    def login_user(self, client, user):
        """Helper to login a user"""
        # Get password based on username
        if user.username == 'user_a':
            password = 'UserAPassword123!'
        elif user.username == 'user_b':
            password = 'UserBPassword123!'
        elif user.username == 'admin':
            password = 'AdminPassword123!'
        else:
            password = 'Password123!'
        
        response = client.post('/auth/login', data={
            'username': user.username,
            'password': password
        }, follow_redirects=False)
        return response
    
    def test_owner_can_access_own_file(self, client, app, user_a, user_a_file):
        """Test that file owner can access their own file"""
        # Login as User A
        self.login_user(client, user_a)
        
        # Try to view User A's file
        response = client.get(f'/file/{user_a_file.id}')
        
        # Should succeed (200 OK)
        assert response.status_code == 200
        assert b'confidential' in response.data
    
    def test_unauthorized_user_cannot_view_file(self, client, app, user_a, user_b, user_a_file):
        """Test that User B cannot view User A's file"""
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to view User A's file
        response = client.get(f'/file/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied (403 Forbidden or redirect with error message)
        assert response.status_code == 200  # Follow redirect
        assert b'permission' in response.data.lower() or b'not authorized' in response.data.lower()
    
    def test_unauthorized_user_cannot_download_file(self, client, app, user_a, user_b, user_a_file):
        """Test that User B cannot download User A's file"""
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to download User A's file
        response = client.get(f'/download/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied
        assert response.status_code == 200  # Follow redirect
        assert b'permission' in response.data.lower() or b'not authorized' in response.data.lower()
    
    def test_unauthorized_user_cannot_delete_file(self, client, app, user_a, user_b, user_a_file):
        """Test that User B cannot delete User A's file"""
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to delete User A's file
        response = client.post(f'/delete/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied
        assert response.status_code == 200  # Follow redirect
        assert b'Only the file owner' in response.data
    
    def test_unauthorized_user_cannot_share_file(self, client, app, user_a, user_b, user_a_file):
        """Test that User B cannot share User A's file"""
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to share User A's file
        response = client.post(f'/share/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied
        assert response.status_code == 200  # Follow redirect
        assert b'Only the file owner' in response.data
    
    def test_shared_recipient_can_access_file(self, client, app, user_a, user_b, user_a_file):
        """Test that User B can access file after User A shares it"""
        # Login as User A
        self.login_user(client, user_a)
        
        # Share User A's file with User B
        share_response = client.post(f'/share/{user_a_file.id}', data={
            'username': 'user_b',
            'permission': 'read'
        }, follow_redirects=True)
        
        assert share_response.status_code == 200
        assert b'successfully' in share_response.data.lower()
        
        # Logout User A
        client.get('/auth/logout')
        
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to view User A's file (now shared)
        response = client.get(f'/file/{user_a_file.id}')
        
        # Should succeed (200 OK)
        assert response.status_code == 200
        assert b'confidential' in response.data
    
    def test_shared_recipient_can_download_file(self, client, app, user_a, user_b, user_a_file):
        """Test that User B can download file after User A shares it"""
        # Login as User A
        self.login_user(client, user_a)
        
        # Share User A's file with User B
        client.post(f'/share/{user_a_file.id}', data={
            'username': 'user_b',
            'permission': 'read'
        }, follow_redirects=True)
        
        # Logout User A
        client.get('/auth/logout')
        
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to download User A's file
        response = client.get(f'/download/{user_a_file.id}')
        
        # Should succeed (200 OK)
        assert response.status_code == 200
    
    def test_unrelated_user_cannot_access(self, client, app, user_a, user_b, user_a_file):
        """Test that User B cannot access before sharing"""
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to view User A's file (not shared yet)
        response = client.get(f'/file/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied
        assert b'permission' in response.data.lower()
    
    def test_write_permission_denied_for_recipient(self, client, app, user_a, user_b, user_a_file):
        """Test that User B with read permission cannot delete User A's file"""
        # Login as User A
        self.login_user(client, user_a)
        
        # Share User A's file with User B (read-only)
        client.post(f'/share/{user_a_file.id}', data={
            'username': 'user_b',
            'permission': 'read'
        }, follow_redirects=True)
        
        # Logout User A
        client.get('/auth/logout')
        
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to delete User A's file (owner-only operation)
        response = client.post(f'/delete/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied (only owner can delete)
        assert b'Only the file owner' in response.data
    
    def test_admin_can_access_all_files(self, client, app, user_a, user_b, user_a_file, user_b_file):
        """Test that admin can access all files"""
        # Login as admin
        self.login_user(client, User.query.filter_by(username='admin').first())
        
        # Try to view User A's file
        response_a = client.get(f'/file/{user_a_file.id}')
        assert response_a.status_code == 200
        
        # Try to view User B's file
        response_b = client.get(f'/file/{user_b_file.id}')
        assert response_b.status_code == 200
    
    def test_non_admin_cannot_access_admin_endpoints(self, client, app, user_a):
        """Test that non-admin cannot access admin endpoints"""
        # Login as User A (not admin)
        self.login_user(client, user_a)
        
        # Try to access admin dashboard
        response = client.get('/admin/dashboard', follow_redirects=False)
        
        # Should be denied (403 Forbidden)
        assert response.status_code == 403
    
    def test_id_enumeration_does_not_bypass_auth(self, client, app, user_a, user_b, user_a_file):
        """Test that guessing file IDs doesn't bypass authorization"""
        # Login as User B
        self.login_user(client, user_b)
        
        # Try to access file with ID that exists but doesn't belong to them
        # This simulates ID enumeration attack
        response = client.get(f'/file/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied despite valid ID
        assert b'permission' in response.data.lower()
    
    def test_share_revocation_prevents_access(self, client, app, user_a, user_b, user_a_file):
        """Test that revoking share prevents access"""
        # Login as User A
        self.login_user(client, user_a)
        
        # Share file with User B
        client.post(f'/share/{user_a_file.id}', data={
            'username': 'user_b',
            'permission': 'read'
        }, follow_redirects=True)
        
        # Get the share ID
        share = FileShare.query.filter_by(
            file_id=user_a_file.id,
            recipient_id=user_b.id
        ).first()
        
        # Logout User A
        client.get('/auth/logout')
        
        # Login as User B and verify access
        self.login_user(client, user_b)
        response_before = client.get(f'/file/{user_a_file.id}')
        assert response_before.status_code == 200
        
        # Logout User B
        client.get('/auth/logout')
        
        # Login as User A and revoke share
        self.login_user(client, user_a)
        client.get(f'/revoke/{share.id}', follow_redirects=True)
        
        # Logout User A
        client.get('/auth/logout')
        
        # Login as User B and verify access is revoked
        self.login_user(client, user_b)
        response_after = client.get(f'/file/{user_a_file.id}', follow_redirects=True)
        
        # Should be denied
        assert b'permission' in response_after.data.lower()
    
    def test_unauthenticated_access_denied(self, client, app, user_a_file):
        """Test that unauthenticated users cannot access files"""
        # No login
        
        # Try to view file
        response = client.get(f'/file/{user_a_file.id}', follow_redirects=True)
        
        # Should redirect to login
        assert response.status_code == 200
        assert b'login' in response.data.lower()


class TestIDOREdgeCases:
    """Test edge cases and IDOR in potential bypass scenarios"""
    
    @pytest.fixture
    def app(self):
        """Create application with test database"""
        app = create_app('testing')
        app.config['TESTING'] = True
        
        with app.app_context():
            db.create_all()
        
        yield app
        
        with app.app_context():
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def user(self, app):
        """Create a test user"""
        with app.app_context():
            user = User(
                username='testuser',
                email='test@example.com',
                is_admin=False
            )
            user.set_password('TestPassword123!')
            db.session.add(user)
            db.session.commit()
            db.session.expunge(user)  # Detach from session
            return user
    
    @pytest.fixture
    def file(self, app, user):
        """Create a test file"""
        with app.app_context():
            import tempfile
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_file.write(b'Test file content')
            temp_file.close()
            
            file = File(
                filename='test_file.txt',
                original_filename='test.txt',
                file_path=temp_file.name,
                file_size=16,
                content_type='text/plain',
                uploader_id=user.id,
                description='Test file'
            )
            db.session.add(file)
            db.session.commit()
            db.session.expunge(file)  # Detach from session
            
            file._temp_path = temp_file.name
            return file
    
    def test_nonexistent_file_returns_404(self, client, file):
        """Test that accessing non-existent file ID returns 404"""
        # Login
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=False)
        
        # Try to access non-existent file ID
        response = client.get('/file/99999')
        
        # Should return 404 Not Found
        assert response.status_code == 404
    
    def test_negative_file_id_handled(self, client, file):
        """Test that negative file ID is handled correctly"""
        # Login
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=False)
        
        # Try to access negative file ID
        response = client.get('/file/-1')
        
        # Should return 404 or error (not 500 which would indicate poor error handling)
        assert response.status_code in [404, 400]
    
    def test_string_file_id_rejected(self, client, file):
        """Test that string file ID is rejected"""
        # Login
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=False)
        
        # Try to access with string ID
        response = client.get('/file/abc')
        
        # Should return 404
        assert response.status_code == 404
    
    def test_authorized_user_can_modify_own_file(self, client, app, user, file):
        """Test that owner can delete their own file"""
        # Login
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=False)
        
        # Delete own file
        response = client.post(f'/delete/{file.id}', follow_redirects=True)
        
        # Should succeed
        assert response.status_code == 200
        assert b'successfully' in response.data.lower()
    
    def test_cascade_delete_with_shares(self, client, app):
        """Test that deleting file cascades to shares"""
        with app.app_context():
            # Create two users
            user1 = User(username='user1', email='user1@example.com', is_admin=False)
            user1.set_password('Password123!')
            user2 = User(username='user2', email='user2@example.com', is_admin=False)
            user2.set_password('Password123!')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            
            # Create file owned by user1
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_file.write(b'Test content')
            temp_file.close()
            
            file = File(
                filename='shared.txt',
                original_filename='shared.txt',
                file_path=temp_file.name,
                file_size=12,
                content_type='text/plain',
                uploader_id=user1.id,
                description='Shared file'
            )
            db.session.add(file)
            db.session.commit()
            
            # Share with user2
            share = FileShare(
                file_id=file.id,
                recipient_id=user2.id,
                shared_by_id=user1.id,
                permission='read'
            )
            db.session.add(share)
            db.session.commit()
            
            share_id = share.id
            file_id = file.id
        
        # Login as user1
        client.post('/auth/login', data={
            'username': 'user1',
            'password': 'Password123!'
        }, follow_redirects=False)
        
        # Delete file
        response = client.post(f'/delete/{file_id}', follow_redirects=True)
        
        # Should succeed
        assert response.status_code == 200
        
        # Verify share is also deleted (cascade)
        with app.app_context():
            deleted_share = FileShare.query.get(share_id)
            assert deleted_share is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
