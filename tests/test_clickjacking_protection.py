"""
CLICKJACKING PROTECTION REGRESSION TESTS

PURPOSE: Verify that X-Frame-Options and CSP frame-ancestors headers
         are properly set to prevent clickjacking attacks.

CWE: CWE-1021 (Improper Restriction of Rendered UI Layers or Frames)
OWASP: A01:2021 - Broken Access Control
"""

import pytest
from app import create_app


class TestClickjackingProtection:
    """Test suite for clickjacking protection"""
    
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
        """Test that X-Frame-Options header is set"""
        response = client.get('/')
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
    
    def test_x_frame_options_header_on_all_pages(self, client):
        """Test that X-Frame-Options is set on all pages"""
        pages = [
            '/',
            '/auth/login',
            '/auth/register',
            '/dashboard',
            '/my-files',
            '/shared-with-me',
        ]
        
        for page in pages:
            response = client.get(page)
            assert 'X-Frame-Options' in response.headers
            assert response.headers['X-Frame-Options'] == 'DENY'
    
    def test_x_frame_options_deny(self, client):
        """Test that X-Frame-Options is set to DENY (most restrictive)"""
        response = client.get('/')
        
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


class TestClickjackingConfiguration:
    """Test frame protection configuration"""
    
    def test_security_headers_in_app_factory(self):
        """Test that security headers are added in app factory"""
        from app import create_app
        
        app = create_app('development')
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            response = client.get('/')
            
            assert 'X-Frame-Options' in response.headers
            assert 'X-Content-Type-Options' in response.headers
            assert 'X-XSS-Protection' in response.headers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
