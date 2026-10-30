import os
import secrets
from flask import render_template, redirect, url_for, flash, request, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import File, FileShare, AuditLog, User
from app.main.forms import FileUploadForm, FileShareForm
from app.main import main_bp


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_secure_filename(original_filename):
    """Generate a secure filename to prevent path traversal and collisions."""
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    secure_name = secure_filename(original_filename)
    if not secure_name:
        secure_name = 'file'
    # Add random token for uniqueness
    return f"{secrets.token_hex(8)}_{secure_name}"


@main_bp.route('/')
def index():
    """Landing page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with statistics."""
    # Statistics
    owned_count = File.query.filter_by(uploader_id=current_user.id).count()
    shared_count = File.query.join(FileShare).filter(
        FileShare.recipient_id == current_user.id
    ).count()
    
    # Recent files
    recent_files = File.query.filter_by(uploader_id=current_user.id).order_by(File.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html', owned_count=owned_count, shared_count=shared_count, recent_files=recent_files)


@main_bp.route('/my-files')
@login_required
def my_files():
    """My Files page - list all files owned by user."""
    owned_files = File.query.filter_by(uploader_id=current_user.id).order_by(File.created_at.desc()).all()
    return render_template('main/my_files.html', files=owned_files)


@main_bp.route('/shared-with-me')
@login_required
def shared_with_me():
    """Shared With Me page - list files shared with user."""
    shared_files = File.query.join(FileShare).filter(
        FileShare.recipient_id == current_user.id
    ).order_by(File.created_at.desc()).all()
    return render_template('main/shared_with_me.html', files=shared_files)


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """File upload endpoint with security validations."""
    form = FileUploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        original_filename = file.filename
        
        if not allowed_file(original_filename):
            flash('Invalid file type.', 'danger')
            return redirect(url_for('main.upload_file'))
        
        # Generate secure filename
        secure_name = generate_secure_filename(original_filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_name)
        
        # Save file
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create database record
        new_file = File(
            filename=secure_name,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            content_type=file.content_type,
            uploader_id=current_user.id,
            description=form.description.data
        )
        db.session.add(new_file)
        db.session.commit()
        
        # Log upload
        audit_log = AuditLog(
            user_id=current_user.id,
            file_id=new_file.id,
            action='upload',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            details=f'File uploaded: {original_filename} ({file_size} bytes)'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/upload.html', form=form)


@main_bp.route('/file/<int:file_id>')
@login_required
def view_file(file_id):
    """View file details."""
    file = File.query.get_or_404(file_id)
    
    # Authorization check
    if not file.is_accessible_by(current_user):
        flash('You do not have permission to access this file.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get share information
    shares = FileShare.query.filter_by(file_id=file_id).all()
    
    return render_template('main/view_file.html', file=file, shares=shares)


@main_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """Secure file download endpoint with authorization."""
    file = File.query.get_or_404(file_id)
    
    # Authorization check
    if not file.is_accessible_by(current_user):
        flash('You do not have permission to download this file.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Log download
    audit_log = AuditLog(
        user_id=current_user.id,
        file_id=file.id,
        action='download',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        details=f'File downloaded: {file.original_filename}'
    )
    db.session.add(audit_log)
    db.session.commit()
    
    # Send file securely
    return send_file(file.file_path, as_attachment=True, download_name=file.original_filename)


@main_bp.route('/share/<int:file_id>', methods=['GET', 'POST'])
@login_required
def share_file(file_id):
    """Share file with another user."""
    file = File.query.get_or_404(file_id)
    
    # Only owner can share
    if not file.is_owned_by(current_user):
        flash('Only the file owner can share this file.', 'danger')
        return redirect(url_for('main.view_file', file_id=file_id))
    
    form = FileShareForm()
    
    if form.validate_on_submit():
        recipient = User.query.filter_by(username=form.username.data).first()
        
        if not recipient:
            flash('User not found.', 'danger')
            return redirect(url_for('main.share_file', file_id=file_id))
        
        if recipient.id == current_user.id:
            flash('You cannot share a file with yourself.', 'danger')
            return redirect(url_for('main.share_file', file_id=file_id))
        
        # Check if already shared
        existing_share = FileShare.query.filter_by(
            file_id=file_id,
            recipient_id=recipient.id
        ).first()
        
        if existing_share:
            flash('File is already shared with this user.', 'warning')
            return redirect(url_for('main.view_file', file_id=file_id))
        
        # Create share
        new_share = FileShare(
            file_id=file_id,
            recipient_id=recipient.id,
            shared_by_id=current_user.id,
            permission=form.permission.data
        )
        db.session.add(new_share)
        db.session.commit()
        
        # Log share
        audit_log = AuditLog(
            user_id=current_user.id,
            file_id=file.id,
            action='share',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            details=f'File shared with {recipient.username} (permission: {form.permission.data})'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash(f'File shared with {recipient.username} successfully!', 'success')
        return redirect(url_for('main.view_file', file_id=file_id))
    
    return render_template('main/share_file.html', file=file, form=form)


@main_bp.route('/revoke/<int:share_id>')
@login_required
def revoke_share(share_id):
    """Revoke file sharing access."""
    share = FileShare.query.get_or_404(share_id)
    file = File.query.get_or_404(share.file_id)
    
    # Only owner can revoke
    if not file.is_owned_by(current_user):
        flash('Only the file owner can revoke access.', 'danger')
        return redirect(url_for('main.view_file', file_id=file.id))
    
    recipient = User.query.get(share.recipient_id)
    
    # Log revoke
    audit_log = AuditLog(
        user_id=current_user.id,
        file_id=file.id,
        action='revoke',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        details=f'Access revoked for {recipient.username}'
    )
    db.session.add(audit_log)
    
    db.session.delete(share)
    db.session.commit()
    
    flash(f'Access revoked for {recipient.username}.', 'success')
    return redirect(url_for('main.view_file', file_id=file.id))


@main_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    """Delete a file (only owner)."""
    file = File.query.get_or_404(file_id)
    
    # Only owner can delete
    if not file.is_owned_by(current_user):
        flash('Only the file owner can delete this file.', 'danger')
        return redirect(url_for('main.view_file', file_id=file_id))
    
    # Log deletion
    audit_log = AuditLog(
        user_id=current_user.id,
        file_id=file.id,
        action='delete',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        details=f'File deleted: {file.original_filename}'
    )
    db.session.add(audit_log)
    
    # Delete file from filesystem
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # Delete from database (cascade will delete shares)
    db.session.delete(file)
    db.session.commit()
    
    flash('File deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))
