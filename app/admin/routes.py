from functools import wraps
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models import User, File, FileShare, AuditLog
from app.admin import admin_bp


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with system overview."""
    # Statistics
    total_users = User.query.count()
    total_files = File.query.count()
    total_shares = FileShare.query.count()
    total_audit_logs = AuditLog.query.count()
    
    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Recent files
    recent_files = File.query.order_by(File.created_at.desc()).limit(10).all()
    
    # Recent audit logs
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(20).all()
    
    return render_template('admin/dashboard.html',
                          total_users=total_users,
                          total_files=total_files,
                          total_shares=total_shares,
                          total_audit_logs=total_audit_logs,
                          recent_users=recent_users,
                          recent_files=recent_files,
                          recent_logs=recent_logs)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """List all users."""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/user/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    """View user details."""
    user = User.query.get_or_404(user_id)
    user_files = File.query.filter_by(uploader_id=user_id).all()
    user_shares = user.shared_with_me.all()
    user_logs = AuditLog.query.filter_by(user_id=user_id).order_by(AuditLog.timestamp.desc()).limit(50).all()
    
    return render_template('admin/view_user.html', user=user, user_files=user_files,
                          user_shares=user_shares, user_logs=user_logs)


@admin_bp.route('/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Toggle admin status for a user."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-demotion
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('admin.view_user', user_id=user_id))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for {user.username}.', 'success')
    return redirect(url_for('admin.view_user', user_id=user_id))


@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user and all associated data."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.view_user', user_id=user_id))
    
    username = user.username
    
    # Delete user (cascade will handle related records)
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/files')
@login_required
@admin_required
def files():
    """List all files."""
    files = File.query.order_by(File.created_at.desc()).all()
    return render_template('admin/files.html', files=files)


@admin_bp.route('/audit-logs')
@login_required
@admin_required
def audit_logs():
    """View audit logs with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    pagination = AuditLog.query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    logs = pagination.items
    
    return render_template('admin/audit_logs.html', logs=logs, pagination=pagination)
