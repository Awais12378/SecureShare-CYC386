#!/usr/bin/env python3
"""
Seed data script for SecureShare.
Creates initial users and test data for development.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, File, FileShare, AuditLog


def seed_data():
    """Seed the database with initial data."""
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        AuditLog.query.delete()
        FileShare.query.delete()
        File.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create users
        print("Creating users...")
        admin = User(
            username='admin',
            email='admin@secureshare.local',
            is_admin=True
        )
        admin.set_password('AdminPassword123!')
        
        user1 = User(
            username='alice',
            email='alice@secureshare.local'
        )
        user1.set_password('AlicePassword123!')
        
        user2 = User(
            username='bob',
            email='bob@secureshare.local'
        )
        user2.set_password('BobPassword123!')
        
        user3 = User(
            username='charlie',
            email='charlie@secureshare.local'
        )
        user3.set_password('CharliePassword123!')
        
        db.session.add_all([admin, user1, user2, user3])
        db.session.commit()
        
        print(f"Created 4 users (admin, alice, bob, charlie)")
        
        # Create test files
        print("Creating test files...")
        import tempfile
        from datetime import datetime
        
        # Create dummy files in upload folder
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # File for alice
        file1_path = os.path.join(upload_folder, 'alice_document.txt')
        with open(file1_path, 'w') as f:
            f.write('This is Alice\'s confidential document.')
        
        file1 = File(
            filename='alice_document.txt',
            original_filename='confidential_document.txt',
            file_path=file1_path,
            file_size=len('This is Alice\'s confidential document.'),
            content_type='text/plain',
            uploader_id=user1.id,
            description='Confidential project document',
            created_at=datetime.utcnow()
        )
        
        # File for bob
        file2_path = os.path.join(upload_folder, 'bob_spreadsheet.xlsx')
        with open(file2_path, 'w') as f:
            f.write('Mock spreadsheet data')
        
        file2 = File(
            filename='bob_spreadsheet.xlsx',
            original_filename='budget_2024.xlsx',
            file_path=file2_path,
            file_size=len('Mock spreadsheet data'),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            uploader_id=user2.id,
            description='Budget spreadsheet for 2024',
            created_at=datetime.utcnow()
        )
        
        # File for admin
        file3_path = os.path.join(upload_folder, 'admin_policy.pdf')
        with open(file3_path, 'w') as f:
            f.write('Security policy document')
        
        file3 = File(
            filename='admin_policy.pdf',
            original_filename='security_policy.pdf',
            file_path=file3_path,
            file_size=len('Security policy document'),
            content_type='application/pdf',
            uploader_id=admin.id,
            description='Company security policy',
            created_at=datetime.utcnow()
        )
        
        db.session.add_all([file1, file2, file3])
        db.session.commit()
        
        print(f"Created 3 test files")
        
        # Create file shares
        print("Creating file shares...")
        share1 = FileShare(
            file_id=file1.id,
            recipient_id=user2.id,
            shared_by_id=user1.id,
            permission='read'
        )
        
        share2 = FileShare(
            file_id=file1.id,
            recipient_id=user3.id,
            shared_by_id=user1.id,
            permission='write'
        )
        
        share3 = FileShare(
            file_id=file2.id,
            recipient_id=user1.id,
            shared_by_id=user2.id,
            permission='read'
        )
        
        db.session.add_all([share1, share2, share3])
        db.session.commit()
        
        print(f"Created 3 file shares")
        
        # Create audit logs
        print("Creating audit logs...")
        audit_logs = [
            AuditLog(user_id=admin.id, action='register', details='Admin user registered'),
            AuditLog(user_id=user1.id, action='register', details='Alice user registered'),
            AuditLog(user_id=user2.id, action='register', details='Bob user registered'),
            AuditLog(user_id=user3.id, action='register', details='Charlie user registered'),
            AuditLog(user_id=user1.id, file_id=file1.id, action='upload', details='File uploaded: confidential_document.txt'),
            AuditLog(user_id=user2.id, file_id=file2.id, action='upload', details='File uploaded: budget_2024.xlsx'),
            AuditLog(user_id=admin.id, file_id=file3.id, action='upload', details='File uploaded: security_policy.pdf'),
            AuditLog(user_id=user1.id, file_id=file1.id, action='share', details='File shared with bob (permission: read)'),
            AuditLog(user_id=user1.id, file_id=file1.id, action='share', details='File shared with charlie (permission: write)'),
        ]
        
        db.session.add_all(audit_logs)
        db.session.commit()
        
        print(f"Created 9 audit logs")
        
        print("\n" + "="*50)
        print("Seed data completed successfully!")
        print("="*50)
        print("\nTest credentials:")
        print("  Admin: admin / AdminPassword123!")
        print("  User 1: alice / AlicePassword123!")
        print("  User 2: bob / BobPassword123!")
        print("  User 3: charlie / CharliePassword123!")
        print("\nRun the application with: python run.py")


if __name__ == '__main__':
    seed_data()
