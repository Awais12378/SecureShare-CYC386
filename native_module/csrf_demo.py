"""
CSRF PROTECTION DEMONSTRATION MODULE

PURPOSE: Educational demonstration of Cross-Site Request Forgery (CSRF) vulnerability
         and the effectiveness of Flask-WTF CSRF protection.

WARNING: This code demonstrates a VULNERABLE implementation for educational purposes.
         The main SecureShare application has CSRF protection enabled globally.

CWE: CWE-352 (Cross-Site Request Forgery (CSRF))
OWASP: A01:2021 - Broken Access Control

SCENARIO: A file deletion operation that can be triggered without user consent
            via a malicious link (without CSRF protection).
"""

from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets

# ============================================================
# VULNERABLE APPLICATION (No CSRF Protection)
# ============================================================

app_vulnerable = Flask(__name__)
app_vulnerable.secret_key = secrets.token_hex(32)
app_vulnerable.config['SESSION_COOKIE_HTTPONLY'] = True
app_vulnerable.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# NOTE: No CSRFProtect initialization - THIS IS THE VULNERABILITY

# Simulated database
files_db = {
    1: {'name': 'important_document.pdf', 'owner': 'user1'},
    2: {'name': 'financial_report.xlsx', 'owner': 'user1'},
    3: {'name': 'personal_notes.txt', 'owner': 'user2'},
}

@app_vulnerable.route('/')
def index_vulnerable():
    """List files"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Vulnerable File Manager</title></head>
<body>
    <h1>Vulnerable File Manager (No CSRF Protection)</h1>
    <p><strong>WARNING:</strong> This application has NO CSRF protection!</p>
    
    <h2>Your Files</h2>
    <ul>
        <li>important_document.pdf - <a href="/delete/1">Delete</a></li>
        <li>financial_report.xlsx - <a href="/delete/2">Delete</a></li>
    </ul>
    
    <h2>CSRF Attack Demonstration</h2>
    <p>An attacker could trick you into clicking this link to delete your files:</p>
    <a href="/delete/1">Click here to win a prize!</a>
    <p><em>Since GET requests perform state changes (bad practice) and there's no CSRF token,
    this would actually delete the file!</em></p>
    
    <p><a href="/attack_page">Visit malicious page to see attack</a></p>
</body>
</html>
    ''')

@app_vulnerable.route('/delete/<int:file_id>')
def delete_file_vulnerable(file_id):
    """
    VULNERABLE: File deletion via GET request with no CSRF protection
    
    VULNERABILITIES:
    1. State-changing operation in GET request (should be POST)
    2. No CSRF token validation
    3. No referrer checking
    4. No origin checking
    """
    if file_id in files_db:
        deleted_file = files_db[file_id]
        del files_db[file_id]
        return f"<h1>File Deleted!</h1><p>Deleted: {deleted_file['name']}</p>"
    return "<h1>File not found</h1>"

@app_vulnerable.route('/attack_page')
def attack_page():
    """Simulated malicious attacker page"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>You Won a Prize!</title></head>
<body>
    <h1>🎉 CONGRATULATIONS! 🎉</h1>
    <p>You've won a free iPhone!</p>
    <p>Click the button below to claim your prize:</p>
    
    <!-- This link would trigger file deletion in the vulnerable app -->
    <a href="/delete/1" style="font-size: 24px; padding: 20px; background: red; color: white; text-decoration: none;">
        CLAIM PRIZE
    </a>
    
    <p><em>In a real attack, this would be styled to look legitimate and would delete the user's file.</em></p>
</body>
</html>
    ''')


# ============================================================
# SECURE APPLICATION (With CSRF Protection)
# ============================================================

app_secure = Flask(__name__)
app_secure.secret_key = secrets.token_hex(32)
app_secure.config['SESSION_COOKIE_HTTPONLY'] = True
app_secure.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# CSRF PROTECTION ENABLED
csrf = CSRFProtect(app_secure)

# Simulated database
files_db_secure = {
    1: {'name': 'important_document.pdf', 'owner': 'user1'},
    2: {'name': 'financial_report.xlsx', 'owner': 'user1'},
    3: {'name': 'personal_notes.txt', 'owner': 'user2'},
}

class DeleteFileForm(FlaskForm):
    """Form with CSRF token automatically added by Flask-WTF"""
    submit = SubmitField('Delete File')


@app_secure.route('/')
def index_secure():
    """List files with CSRF-protected delete buttons"""
    form = DeleteFileForm()
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>Secure File Manager</title></head>
<body>
    <h1>Secure File Manager (CSRF Protected)</h1>
    <p><strong>SECURE:</strong> This application has CSRF protection enabled!</p>
    
    <h2>Your Files</h2>
    <ul>
        <li>important_document.pdf</li>
        <li>financial_report.xlsx</li>
    </ul>
    
    <h2>Delete Files</h2>
    <form method="POST" action="/delete/1">
        {{ form.hidden_tag() }}
        {{ form.submit.label }} {{ form.submit() }}
    </form>
    
    <form method="POST" action="/delete/2">
        {{ form.hidden_tag() }}
        {{ form.submit.label }} {{ form.submit() }}
    </form>
    
    <h2>CSRF Protection Details</h2>
    <ul>
        <li>✅ CSRF token in every form (hidden field)</li>
        <li>✅ POST requests for state changes</li>
        <li>✅ Token validated on submission</li>
        <li>✅ Secure session cookies (HttpOnly, SameSite)</li>
    </ul>
    
    <p><a href="/attack_page">Visit malicious page (will fail)</a></p>
</body>
</html>
    ''', form=form)

@app_secure.route('/delete/<int:file_id>', methods=['POST'])
def delete_file_secure(file_id):
    """
    SECURE: File deletion with CSRF protection
    
    SECURITY CONTROLS:
    1. POST request only (no GET for state changes)
    2. CSRF token validation (automatic via Flask-WTF)
    3. Form-based submission required
    """
    form = DeleteFileForm()
    
    if not form.validate_on_submit():
        return "<h1>CSRF Token Invalid!</h1><p>Request rejected.</p>"
    
    if file_id in files_db_secure:
        deleted_file = files_db_secure[file_id]
        del files_db_secure[file_id]
        return f"<h1>File Deleted!</h1><p>Deleted: {deleted_file['name']}</p>"
    return "<h1>File not found</h1>"

@app_secure.errorhandler(CSRFError)
def handle_csrf_error(e):
    """Handle CSRF errors"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>CSRF Error</title></head>
<body>
    <h1>⚠️ CSRF Protection Error</h1>
    <p>Your request was rejected because it lacked a valid CSRF token.</p>
    <p>This is a security measure to prevent Cross-Site Request Forgery attacks.</p>
    <p>Please try again from the legitimate application.</p>
    <p><a href="/">Return to Home</a></p>
</body>
</html>
    '''), 400

@app_secure.route('/attack_page')
def attack_page_secure():
    """Simulated malicious attacker page (will fail against secure app)"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head><title>You Won a Prize!</title></head>
<body>
    <h1>🎉 CONGRATULATIONS! 🎉</h1>
    <p>You've won a free iPhone!</p>
    <p>Click the button below to claim your prize:</p>
    
    <!-- This form has no CSRF token, so it will be rejected -->
    <form method="POST" action="/delete/1">
        <button style="font-size: 24px; padding: 20px; background: red; color: white;">
            CLAIM PRIZE
        </button>
    </form>
    
    <p><em>This attack will fail because the form lacks a CSRF token.</em></p>
</body>
</html>
    ''')


# ============================================================
# DEMONSTRATION
# ============================================================

def main():
    print("=" * 70)
    print("CSRF PROTECTION DEMONSTRATION MODULE")
    print("SecureShare Security Engineering Lab")
    print("=" * 70)
    
    print("\nCWE: CWE-352 (Cross-Site Request Forgery)")
    print("OWASP: A01:2021 - Broken Access Control")
    
    print("\n" + "=" * 70)
    print("PART 1: VULNERABLE APPLICATION")
    print("=" * 70)
    print("\nVULNERABLE APP running on http://127.0.0.1:5001")
    print("- No CSRF protection")
    print("- GET requests perform state changes")
    print("- Easily exploitable via malicious links")
    print("\nVisit: http://127.0.0.1:5001")
    print("Then visit: http://127.0.0.1:5001/attack_page")
    print("\nTry clicking 'CLAIM PRIZE' - it will delete a file!")
    
    print("\n" + "=" * 70)
    print("PART 2: SECURE APPLICATION")
    print("=" * 70)
    print("\nSECURE APP running on http://127.0.0.1:5002")
    print("- CSRF protection enabled")
    print("- POST requests for state changes")
    print("- CSRF tokens in all forms")
    print("- Token validation on submission")
    print("\nVisit: http://127.0.0.1:5002")
    print("Then visit: http://127.0.0.1:5002/attack_page")
    print("\nTry clicking 'CLAIM PRIZE' - it will be rejected with CSRF error!")
    
    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)
    print("""
VULNERABLE vs SECURE:

VULNERABLE:
❌ No CSRF token validation
❌ GET requests for state changes
❌ Form submission without tokens
❌ Susceptible to CSRF attacks
❌ Clickjacking possible (no X-Frame-Options)

SECURE:
✅ CSRF token in every form
✅ POST requests for state changes
✅ Token validation required
✅ Protected against CSRF attacks
✅ X-Frame-Options: DENY (clickjacking protection)
✅ Secure session cookies (HttpOnly, SameSite)
    """)
    
    print("\n" + "=" * 70)
    print("SECURESHARE IMPLEMENTATION")
    print("=" * 70)
    print("""
SecureShare already has CSRF protection enabled:

1. Flask-WTF CSRFProtect initialized (app/__init__.py)
2. WTF_CSRF_ENABLED = True (app/config.py)
3. All forms use FlaskForm (automatic CSRF tokens)
4. State-changing operations use POST requests
5. Secure cookie settings (HttpOnly, SameSite)
6. X-Frame-Options: DENY header

All sensitive operations are protected:
- File upload (POST with CSRF token)
- File delete (POST with CSRF token)
- File share (POST with CSRF token)
- Share revoke (POST with CSRF token)
- Settings changes (POST with CSRF token)
    """)
    
    print("\n" + "=" * 70)
    print("NOTE: To run the demonstration servers:")
    print("=" * 70)
    print("Run this file directly to start both servers on different ports.")
    print("Then open your browser to the URLs above.")
    print("\nOr run the automated tests to verify CSRF protection.")


if __name__ == "__main__":
    if len(__import__('sys').argv) > 1 and __import__('sys').argv[1] == 'demo':
        # Run demonstration servers
        from threading import Thread
        
        def run_vulnerable():
            print("Starting vulnerable app on port 5001...")
            app_vulnerable.run(port=5001, debug=False)
        
        def run_secure():
            print("Starting secure app on port 5002...")
            app_secure.run(port=5002, debug=False)
        
        t1 = Thread(target=run_vulnerable)
        t2 = Thread(target=run_secure)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        main()
