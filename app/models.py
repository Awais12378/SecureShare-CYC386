from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and authorization."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    uploaded_files = db.relationship('File', backref='uploader', lazy='dynamic',
                                      foreign_keys='File.uploader_id')
    shared_with_me = db.relationship('FileShare', backref='recipient', lazy='dynamic',
                                      foreign_keys='FileShare.recipient_id')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic',
                                  foreign_keys='AuditLog.user_id')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class File(db.Model):
    """File model for uploaded files."""
    
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(100))
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    shares = db.relationship('FileShare', backref='file', lazy='dynamic',
                            cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='file', lazy='dynamic',
                                  foreign_keys='AuditLog.file_id')
    
    def is_owned_by(self, user):
        """Check if file is owned by user."""
        return self.uploader_id == user.id
    
    def is_accessible_by(self, user):
        """Check if file is accessible by user (owner or shared)."""
        if self.is_owned_by(user):
            return True
        return FileShare.query.filter_by(
            file_id=self.id,
            recipient_id=user.id
        ).first() is not None
    
    def __repr__(self):
        return f'<File {self.original_filename}>'


class FileShare(db.Model):
    """File sharing model for access control."""
    
    __tablename__ = 'file_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shared_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    permission = db.Column(db.String(20), default='read', nullable=False)  # 'read' or 'write'
    
    # Relationship for shared_by
    shared_by = db.relationship('User', foreign_keys=[shared_by_id])
    
    # Unique constraint to prevent duplicate shares
    __table_args__ = (db.UniqueConstraint('file_id', 'recipient_id', name='unique_file_share'),)
    
    def __repr__(self):
        return f'<FileShare file_id={self.file_id} recipient_id={self.recipient_id}>'


class AuditLog(db.Model):
    """Audit log model for tracking security-relevant events."""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for system events
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # e.g., 'upload', 'download', 'share', 'revoke'
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    details = db.Column(db.Text)  # Additional context
    
    def __repr__(self):
        return f'<AuditLog {self.action} by user_id={self.user_id} at {self.timestamp}>'
