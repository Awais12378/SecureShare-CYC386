from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User, AuditLog
from app.auth.forms import RegistrationForm, LoginForm
from app.auth import auth_bp


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Log registration
        audit_log = AuditLog(
            user_id=user.id,
            action='register',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            details=f'New user registered: {user.username}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            # Log failed login attempt
            audit_log = AuditLog(
                user_id=user.id if user else None,
                action='login_failed',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                details=f'Failed login attempt for username: {form.username.data}'
            )
            db.session.add(audit_log)
            db.session.commit()
            
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        # Log successful login
        audit_log = AuditLog(
            user_id=user.id,
            action='login',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            details=f'User logged in: {user.username}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        login_user(user, remember=form.remember_me.data)
        flash('You have been logged in successfully.', 'success')
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.dashboard')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """User logout endpoint."""
    if current_user.is_authenticated:
        # Log logout
        audit_log = AuditLog(
            user_id=current_user.id,
            action='logout',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            details=f'User logged out: {current_user.username}'
        )
        db.session.add(audit_log)
        db.session.commit()
        
        logout_user()
        flash('You have been logged out.', 'info')
    
    return redirect(url_for('auth.login'))
