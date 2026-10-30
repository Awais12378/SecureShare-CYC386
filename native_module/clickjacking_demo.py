"""
CLICKJACKING PROTECTION DEMONSTRATION MODULE

PURPOSE: Educational demonstration of Clickjacking vulnerability and
         the effectiveness of X-Frame-Options and CSP frame-ancestors protection.

WARNING: This code demonstrates a VULNERABLE implementation for educational purposes.
         The main SecureShare application has frame protection enabled.

CWE: CWE-1021 (Improper Restriction of Rendered UI Layers or Frames)
OWASP: A01:2021 - Broken Access Control

SCENARIO: A malicious website attempts to frame the SecureShare application
            to trick users into clicking buttons they can't see.
"""

from flask import Flask, render_template_string, make_response

# ============================================================
# VULNERABLE APPLICATION (No Frame Protection)
# ============================================================

app_vulnerable = Flask(__name__)
app_vulnerable.secret_key = 'vulnerable-secret-key'


@app_vulnerable.route('/')
def index_vulnerable():
    """Vulnerable page with no frame protection"""
    response = make_response(render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .danger-zone {
            background: #ffebee;
            border: 2px solid #f44336;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        button {
            padding: 15px 30px;
            font-size: 18px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <h1>Vulnerable Page (No Frame Protection)</h1>
    <p><strong>WARNING:</strong> This page has NO frame protection!</p>
    <p>It can be embedded in an iframe by any website, making it vulnerable to clickjacking attacks.</p>
    
    <div class="danger-zone">
        <h2>Dangerous Action</h2>
        <p>This button performs a sensitive action (simulated):</p>
        <button onclick="alert('File deleted! In a real attack, this would happen without user knowledge.')">
            Delete All Files
        </button>
    </div>
    
    <h2>Clickjacking Attack Scenario</h2>
    <p>An attacker could embed this page in an invisible iframe and overlay a fake "Claim Prize" button:</p>
    <pre>
&lt;iframe src="http://vulnerable-app.com/" 
        style="opacity: 0.01; position: absolute; top: 0; left: 0; width: 100%; height: 100%;"&gt;
&lt;/iframe&gt;
&lt;button style="position: absolute; top: 50%; left: 50%;"&gt;
    Claim Free iPhone!
&lt;/button&gt;
    </pre>
    
    <p>When the user clicks "Claim Free iPhone!", they're actually clicking the invisible "Delete All Files" button.</p>
</body>
</html>
    '''))
    
    # NO X-Frame-Options header - THIS IS THE VULNERABILITY
    return response


@app_vulnerable.route('/attacker')
def attacker_page():
    """Simulated attacker page that performs clickjacking"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>You Won a Prize!</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        .prize {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            margin: 50px auto;
            max-width: 600px;
        }
        button {
            padding: 20px 40px;
            font-size: 24px;
            background: #ffeb3b;
            color: #333;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.01;
            z-index: 1;
        }
        .overlay {
            position: relative;
            z-index: 2;
        }
    </style>
</head>
<body>
    <!-- Vulnerable page embedded in invisible iframe -->
    <iframe src="/"></iframe>
    
    <div class="overlay">
        <div class="prize">
            <h1>🎉 CONGRATULATIONS! 🎉</h1>
            <h2>You've Won a Free iPhone 15 Pro!</h2>
            <p>Click the button below to claim your prize:</p>
            <button>CLAIM PRIZE NOW</button>
            <p><em> positioned exactly over the "Delete All Files" button</em></p>
        </div>
    </div>
</body>
</html>
    ''')


# ============================================================
# SECURE APPLICATION (With Frame Protection)
# ============================================================

app_secure = Flask(__name__)
app_secure.secret_key = 'secure-secret-key'


@app_secure.route('/')
def index_secure():
    """Secure page with frame protection"""
    response = make_response(render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Secure Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .safe-zone {
            background: #e8f5e9;
            border: 2px solid #4CAF50;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        button {
            padding: 15px 30px;
            font-size: 18px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Secure Page (Frame Protected)</h1>
    <p><strong>SECURE:</strong> This page has frame protection enabled!</p>
    <p>It cannot be embedded in an iframe by any website, preventing clickjacking attacks.</p>
    
    <div class="safe-zone">
        <h2>Protected Action</h2>
        <p>This button performs a sensitive action (simulated):</p>
        <button onclick="alert('Action protected! This page cannot be framed.')">
            Delete All Files
        </button>
    </div>
    
    <h2>Protection Mechanisms</h2>
    <ul>
        <li>✅ X-Frame-Options: DENY header</li>
        <li>✅ Content-Security-Policy: frame-ancestors 'none'</li>
        <li>✅ Page cannot be embedded in any iframe</li>
        <li>✅ Clickjacking attacks prevented</li>
    </ul>
    
    <h2>Clickjacking Attack Blocked</h2>
    <p>An attacker attempting to embed this page would see:</p>
    <pre>
refused to display 'http://secure-app.com/' in a frame because it set 
'X-Frame-Options' to 'deny'.
    </pre>
</body>
</html>
    '''))
    
    # FRAME PROTECTION ENABLED
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
    
    return response


@app_secure.route('/attacker')
def attacker_page_secure():
    """Simulated attacker page (blocked by frame protection)"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>You Won a Prize!</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        .prize {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            margin: 50px auto;
            max-width: 600px;
        }
        button {
            padding: 20px 40px;
            font-size: 24px;
            background: #ffeb3b;
            color: #333;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
        }
        iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.01;
            z-index: 1;
        }
        .overlay {
            position: relative;
            z-index: 2;
        }
    </style>
</head>
<body>
    <!-- Attempt to embed secure page (will be blocked) -->
    <iframe src="/"></iframe>
    
    <div class="overlay">
        <div class="prize">
            <h1>🎉 CONGRATULATIONS! 🎉</h1>
            <h2>You've Won a Free iPhone 15 Pro!</h2>
            <p>Click the button below to claim your prize:</p>
            <button>CLAIM PRIZE NOW</button>
            <p><em>The iframe above will be blocked by browser security</em></p>
        </div>
    </div>
</body>
</html>
    ''')


# ============================================================
# DEMONSTRATION
# ============================================================

def main():
    print("=" * 70)
    print("CLICKJACKING PROTECTION DEMONSTRATION MODULE")
    print("SecureShare Security Engineering Lab")
    print("=" * 70)
    
    print("\nCWE: CWE-1021 (Improper Restriction of Rendered UI Layers or Frames)")
    print("OWASP: A01:2021 - Broken Access Control")
    
    print("\n" + "=" * 70)
    print("PART 1: VULNERABLE APPLICATION")
    print("=" * 70)
    print("\nVULNERABLE APP running on http://127.0.0.1:5003")
    print("- No X-Frame-Options header")
    print("- No CSP frame-ancestors")
    print("- Can be embedded in any iframe")
    print("- Susceptible to clickjacking attacks")
    print("\nVisit: http://127.0.0.1:5003")
    print("Then visit: http://127.0.0.1:5003/attacker")
    print("\nThe attacker page will successfully embed the vulnerable page.")
    print("Click 'CLAIM PRIZE' - it will trigger the hidden action!")
    
    print("\n" + "=" * 70)
    print("PART 2: SECURE APPLICATION")
    print("=" * 70)
    print("\nSECURE APP running on http://127.0.0.1:5004")
    print("- X-Frame-Options: DENY header")
    print("- CSP frame-ancestors 'none'")
    print("- Cannot be embedded in any iframe")
    print("- Protected against clickjacking attacks")
    print("\nVisit: http://127.0.0.1:5004")
    print("Then visit: http://127.0.0.1:5004/attacker")
    print("\nThe attacker page will be blocked by browser security.")
    print("The iframe will show 'refused to display in a frame' error.")
    
    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)
    print("""
VULNERABLE vs SECURE:

VULNERABLE:
❌ No X-Frame-Options header
❌ No CSP frame-ancestors
❌ Can be embedded in any iframe
❌ Susceptible to clickjacking
❌ User can be tricked into clicking hidden buttons

SECURE:
✅ X-Frame-Options: DENY header
✅ CSP frame-ancestors 'none'
✅ Cannot be embedded in any iframe
✅ Protected against clickjacking
✅ Browser blocks framing attempts
✅ User cannot be tricked
    """)
    
    print("\n" + "=" * 70)
    print("SECURESHARE IMPLEMENTATION")
    print("=" * 70)
    print("""
SecureShare already has clickjacking protection enabled:

1. X-Frame-Options: DENY header (app/__init__.py)
2. Applied to all responses globally
3. Prevents any website from framing SecureShare
4. Complementary to CSRF protection
5. Defense in depth against UI redress attacks

All pages are protected:
- Login page
- Dashboard
- File view/delete/share pages
- Admin pages
- Settings pages
    """)
    
    print("\n" + "=" * 70)
    print("FRAME PROTECTION OPTIONS")
    print("=" * 70)
    print("""
X-Frame-Options Values:

1. DENY
   - No framing allowed by any site
   - Most restrictive
   - SecureShare uses this

2. SAMEORIGIN
   - Only framing by same origin allowed
   - Allows internal framing if needed

3. ALLOW-FROM uri
   - Deprecated, not recommended

CSP frame-ancestors Values:

1. 'none'
   - No framing allowed
   - SecureShare uses this

2. 'self'
   - Only same origin can frame

3. 'self' https://trusted.com
   - Same origin and specific trusted sites
    """)
    
    print("\n" + "=" * 70)
    print("BROWSER SUPPORT")
    print("=" * 70)
    print("""
X-Frame-Options:
- Supported by all modern browsers
- Can be superseded by CSP frame-ancestors

CSP frame-ancestors:
- Supported by Chrome, Firefox, Safari, Edge
- More flexible than X-Frame-Options
- Can specify multiple allowed origins

Recommendation: Use both for maximum compatibility
- X-Frame-Options: DENY (for older browsers)
- CSP frame-ancestors 'none' (for modern browsers)
    """)
    
    print("\n" + "=" * 70)
    print("NOTE: To run the demonstration servers:")
    print("=" * 70)
    print("Run this file directly to start both servers on different ports.")
    print("Then open your browser to the URLs above.")
    print("\nOr run the automated tests to verify frame protection.")


if __name__ == "__main__":
    if len(__import__('sys').argv) > 1 and __import__('sys').argv[1] == 'demo':
        # Run demonstration servers
        from threading import Thread
        
        def run_vulnerable():
            print("Starting vulnerable app on port 5003...")
            app_vulnerable.run(port=5003, debug=False)
        
        def run_secure():
            print("Starting secure app on port 5004...")
            app_secure.run(port=5004, debug=False)
        
        t1 = Thread(target=run_vulnerable)
        t2 = Thread(target=run_secure)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        main()
