import pytest
from app import db
from app.models import User, File, AuditLog


def test_admin_dashboard_requires_admin(logged_in_client):
    """Test that admin dashboard requires admin role."""
    response = logged_in_client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 403


def test_admin_dashboard_accessible_by_admin(admin_client):
    """Test that admin can access admin dashboard."""
    response = admin_client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data


def test_admin_users_requires_admin(logged_in_client):
    """Test that users page requires admin role."""
    response = logged_in_client.get('/admin/users', follow_redirects=True)
    assert response.status_code == 403


def test_admin_users_accessible_by_admin(admin_client):
    """Test that admin can access users page."""
    response = admin_client.get('/admin/users')
    assert response.status_code == 200
    assert b'Users' in response.data


def test_admin_view_user_requires_admin(logged_in_client, init_db):
    """Test that view user requires admin role."""
    response = logged_in_client.get('/admin/user/1', follow_redirects=True)
    assert response.status_code == 403


def test_admin_view_user_accessible_by_admin(admin_client, init_db):
    """Test that admin can view user details."""
    with init_db:
        user_id = init_db['user1'].id
    
    response = admin_client.get(f'/admin/user/{user_id}')
    assert response.status_code == 200


def test_admin_toggle_admin(admin_client, init_db):
    """Test that admin can toggle admin status."""
    with init_db:
        user_id = init_db['user2'].id
    
    response = admin_client.post(f'/admin/user/{user_id}/toggle-admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin privileges granted' in response.data
    
    with init_db:
        user = User.query.get(user_id)
        assert user.is_admin is True


def test_admin_cannot_toggle_own_status(admin_client, init_db):
    """Test that admin cannot toggle their own status."""
    with init_db:
        admin_id = init_db['admin'].id
    
    response = admin_client.post(f'/admin/user/{admin_id}/toggle-admin', follow_redirects=True)
    assert b'cannot change your own' in response.data


def test_admin_delete_user(admin_client, init_db):
    """Test that admin can delete user."""
    with init_db:
        user_id = init_db['user2'].id
    
    response = admin_client.post(f'/admin/user/{user_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'has been deleted' in response.data
    
    with init_db:
        user = User.query.get(user_id)
        assert user is None


def test_admin_cannot_delete_self(admin_client, init_db):
    """Test that admin cannot delete themselves."""
    with init_db:
        admin_id = init_db['admin'].id
    
    response = admin_client.post(f'/admin/user/{admin_id}/delete', follow_redirects=True)
    assert b'cannot delete your own' in response.data


def test_admin_files_requires_admin(logged_in_client):
    """Test that files page requires admin role."""
    response = logged_in_client.get('/admin/files', follow_redirects=True)
    assert response.status_code == 403


def test_admin_files_accessible_by_admin(admin_client):
    """Test that admin can access files page."""
    response = admin_client.get('/admin/files')
    assert response.status_code == 200
    assert b'All Files' in response.data


def test_admin_audit_logs_requires_admin(logged_in_client):
    """Test that audit logs page requires admin role."""
    response = logged_in_client.get('/admin/audit-logs', follow_redirects=True)
    assert response.status_code == 403


def test_admin_audit_logs_accessible_by_admin(admin_client):
    """Test that admin can access audit logs page."""
    response = admin_client.get('/admin/audit-logs')
    assert response.status_code == 200
    assert b'Audit Logs' in response.data


def test_admin_dashboard_shows_statistics(admin_client, init_db):
    """Test that admin dashboard shows correct statistics."""
    response = admin_client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'3' in response.data  # 3 users created in init_db


def test_non_admin_cannot_access_admin_routes(logged_in_client):
    """Test that non-admin cannot access any admin routes."""
    routes = [
        '/admin/dashboard',
        '/admin/users',
        '/admin/files',
        '/admin/audit-logs'
    ]
    
    for route in routes:
        response = logged_in_client.get(route)
        assert response.status_code == 403
