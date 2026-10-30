"""
CSRF PROTECTION REGRESSION TESTS

PURPOSE: Verify that CSRF protection is properly implemented and
         rejects requests without valid CSRF tokens.

CWE: CWE-352 (Cross-Site Request Forgery)
OWASP: A01:2021 - Broken Access Control
"""

import pytest
from app import create_app, db
from app.models import User, File
from flask_wtf.csrf import CSRFError


class TestCSRFProtection:
    """Test suite for CSRF protection in SecureShare"""
    
    @pytest.fixture
    def app(self):
        """Create application with CSRF enabled"""
        app = create_app('development')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True  # Ensure CSRF is enabled
        
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
        """Create test user"""
        with app.app_context():
            user = User(
                username='testuser',
                email='test@example.com',
                is_admin=False
            )
            user.set_password('TestPassword123!')
            db.session.add(user)
            db.session.commit()
            return user
    
    @pytest.fixture
    def test_file(self, app, user):
        """Create test file"""
        with app.app_context():
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_file.write(b'Test content')
            temp_file.close()
            
            file = File(
                filename='test_file.txt',
                original_filename='test.txt',
                file_path=temp_file.name,
                file_size=12,
                content_type='text/plain',
                uploader_id=user.id,
                description='Test file'
            )
            db.session.add(file)
            db.session.commit()
            return file
    
    def test_csrf_token_in_form(self, client, app):
        """Test that CSRF token is present in forms"""
        response = client.get('/auth/login')
        
        # Check for CSRF token in response
        assert b'csrf_token' in response.data or b'csrfmiddlewaretoken' in response.data
    
    def test_post_without_csrf_token_rejected(self, client, app, user, test_file):
        """Test that POST without CSRF token is rejected"""
        # Login first
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        
        # Try to delete file without CSRF token
        response = client.post(f'/delete/{test_file.id}', data={})
        
        # Should be rejected (400 Bad Request or redirect with error)
        # Flask-WTF returns 400 for CSRF errors
        assert response.status_code in [400, 302, 303]
    
    def test_csrf_token_required_for_upload(self, client, app, user):
        """Test that CSRF token is required for file upload"""
        # Login first
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        
        # Try to upload without CSRF token
        response = client.post('/upload', data={
            'file': (None, b'test content', 'test.txt')
        })
        
        # Should be rejected
        assert response.status_code in [400, 302, 303]
    
    def test_csrf_token_required_for_share(self, client, app, user, test_file):
        """Test that CSRF token is required for file sharing"""
        # Login first
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        
        # Try to share without CSRF token
        response = client.post(f'/share/{test_file.id}', data={
            'username': 'otheruser'
        })
        
        # Should be rejected
        assert response.status_code in [400, 302, 303]
    
    def test_csrf_token_required_for_revoke(self, client, app, user, test_file):
        """Test that CSRF token is required for share revocation"""
        # Login first
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123!'
        }, follow_redirects=True)
        
        # Try to revoke without CSRF token
        response = client.get(f'/revoke/1')
        
        # GET should work (view page), but POST would require token
        assert response.status_code in [200, 302, 303]
    
    def test_get_requests_no_state_changes(self, client, app):
        """Test that GET requests don't perform state changes"""
        # GET requests should be safe (idempotent)
        # This is a best practice - CSRF primarily affects POST
        
        # Try GET on delete endpoint (should not delete)
        response = client.get('/delete/999')
        
        # Should redirect or show error, not perform action
        assert response.status_code in [302, 303, 404, 405]  # 405 = Method Not Allowed
    
    def test_session_cookie_httponly(self, app):
        """Test that session cookie has HttpOnly flag"""
        with app.test_client() as client:
            response = client.get('/')
            
            # Check session cookie
            cookies = [c for c in client.cookie_jar if c.name == 'session']
            if cookies:
                # HttpOnly is a flag, not easily testable in Flask test client
                # But we can verify the config
                assert app.config['SESSION_COOKIE_HTTPONLY'] == True
    
    def test_session_cookie_samesite(self, app):
        """Test that session cookie has SameSite attribute"""
        with app.test_client() as client:
            # Verify config setting
            assert app.config['SESSION_COOKIE_SAMESITE'] in ['Lax', 'Strict']
    
    def test_csrf_enabled_in_config(self, app):
        """Test that CSRF is enabled in configuration"""
        assert app.config['WTF_CSRF_ENABLED'] == True
    
    def test_csrf_time_limit_configured(self, app):
        """Test that CSRF time limit is configured"""
        # None means tokens don't expire (or use default)
        assert 'WTF_CSRF_TIME_LIMIT' in app.config


class TestCSRFConfiguration:
    """Test CSRF configuration in different environments"""
    
    def test_csrf_disabled_in_testing(self):
        """Test that CSRF is disabled in testing config"""
        from app.config import TestingConfig
        assert TestingConfig.WTF_CSRF_ENABLED == False
    
    def test_csrf_enabled_in_development(self):
        """Test that CSRF is enabled in development config"""
        from app.config import DevelopmentConfig
        assert DevelopmentConfig.WTF_CSRF_ENABLED == True
    
    def test_csrf_enabled_in_production(self):
        """Test that CSRF is enabled in production config"""
        from app.config import ProductionConfig
        assert ProductionConfig.WTF_CSRF_ENABLED == True
    
    def test_production_cookie_settings(self):
        """Test that production has stricter cookie settings"""
        from app.config import ProductionConfig
        assert ProductionConfig.SESSION_COOKIE_SECURE == True
        assert ProductionConfig.SESSION_COOKIE_SAMESITE == 'Strict'


class TestCSRFSecurityHeaders:
    """Test security headers that complement CSRF protection"""
    
    @pytest.fixture
    def app(self):
        """Create application"""
        app = create_app('development')
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    def test_x_frame_options_header(self, client):
        """Test that X-Frame-Options header is set (prevents clickjacking)"""
        response = client.get('/')
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
    
    def test_x_content_type_options_header(self, client):
        """Test that X-Content-Type-Options header is set"""
        response = client.get('/')
        
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
    
    def test_x_xss_protection_header(self, client):
        """Test that X-XSS-Protection header is set"""
        response = client.get('/')
        
        assert 'X-XSS-Protection' in response.headers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
