#!/usr/bin/env python3
"""
Clear all users except admin from the database.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, File, FileShare, AuditLog


def clear_non_admin_users():
    """Delete all users except admin and their associated data."""
    app = create_app('development')
    
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("ERROR: Admin user not found!")
            return
        
        print(f"Admin user found: {admin.username}")
        
        # Get all non-admin users
        non_admin_users = User.query.filter(User.username != 'admin').all()
        
        if not non_admin_users:
            print("No non-admin users found. Database is already clean.")
            return
        
        print(f"\nFound {len(non_admin_users)} non-admin user(s) to delete:")
        for user in non_admin_users:
            print(f"  - {user.username} ({user.email})")
        
        # Delete data associated with non-admin users
        print("\nDeleting associated data...")
        
        # Delete audit logs for non-admin users
        deleted_audit_logs = AuditLog.query.filter(
            AuditLog.user_id.in_([u.id for u in non_admin_users])
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_audit_logs} audit log entries")
        
        # Delete file shares where non-admin users are recipients or sharers
        deleted_shares_as_recipient = FileShare.query.filter(
            FileShare.recipient_id.in_([u.id for u in non_admin_users])
        ).delete(synchronize_session=False)
        deleted_shares_as_sharer = FileShare.query.filter(
            FileShare.shared_by_id.in_([u.id for u in non_admin_users])
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_shares_as_recipient + deleted_shares_as_sharer} file share entries")
        
        # Delete files uploaded by non-admin users
        deleted_files = File.query.filter(
            File.uploader_id.in_([u.id for u in non_admin_users])
        ).delete(synchronize_session=False)
        print(f"  Deleted {deleted_files} file entries")
        
        # Delete the users
        deleted_users = User.query.filter(User.username != 'admin').delete(synchronize_session=False)
        print(f"  Deleted {deleted_users} user(s)")
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("Non-admin users deleted successfully!")
        print("="*50)
        print("\nRemaining users:")
        print(f"  Admin: admin / AdminPassword123!")
        print("\nYou can now create your own users through the registration page.")


if __name__ == '__main__':
    clear_non_admin_users()
