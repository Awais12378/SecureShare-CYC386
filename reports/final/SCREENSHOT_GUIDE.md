# Screenshot Capture Guide

**SecureShare CYC386 Midterm Lab Exam Report**  
**Date:** October 30, 2026  
**Purpose:** Complete instructions for capturing all required screenshots

---

## Screenshot Summary Table

| Screenshot ID | Screenshot Title | Tool / Location | Report Section | Status |
|---------------|-----------------|-----------------|----------------|--------|
| SS-01 | SecureShare Login Interface | SecureShare browser | Section 3.11 | Not captured |
| SS-02 | SecureShare User Dashboard | SecureShare browser | Section 3.11 | Not captured |
| SS-03 | SecureShare File Upload Interface | SecureShare browser | Section 3.11 | Not captured |
| SS-04 | Buffer Overflow Before Fix - ASAN Output | Local C lab / terminal | Section 8.1 | Not captured |
| SS-05 | Buffer Overflow After Fix - Secure Output | Local C lab / terminal | Section 8.1 | Not captured |
| SS-06 | Command Injection Before Fix | Local lab / terminal | Section 8.2 | Not captured |
| SS-07 | Command Injection After Fix | Local lab / terminal | Section 8.2 | Not captured |
| SS-08 | IDOR Before Fix - Unauthorized Access | SecureShare browser | Section 8.3 | Not captured |
| SS-09 | IDOR After Fix - Authorized Access | SecureShare browser | Section 8.3 | Not captured |
| SS-10 | CSRF Before Fix - Vulnerable Execution | Local demo / browser | Section 8.4 | Not captured |
| SS-11 | CSRF After Fix - Token Rejection | Local demo / browser | Section 8.4 | Not captured |
| SS-12 | Clickjacking Before Fix - Iframe Embed | Local demo / browser | Section 8.5 | Not captured |
| SS-13 | Clickjacking After Fix - Iframe Blocked | Local demo / browser | Section 8.5 | Not captured |
| SS-14 | SAST Scan Results - Semgrep Output | Semgrep / terminal | Section 9.1 | Available in pipeline_results |
| SS-15 | DAST Scan Results - OWASP ZAP Report | OWASP ZAP / browser | Section 9.2 | Not captured |
| SS-16 | GitHub Actions Pipeline Success | GitHub / browser | Section 10.9 | Not captured |
| SS-17 | GitHub Actions Pipeline Failure | GitHub / browser | Section 10.9 | Not captured |
| SS-18 | Jira Sprint Board | Jira / browser | Section 13.3 | Not captured |
| SS-19 | GitHub Pull Request Review | GitHub / browser | Section 13.7 | Not captured |

---

## Detailed Screenshot Instructions

### SS-01: SecureShare Login Interface

**Screenshot Title:** SecureShare Login Interface  
**Report Section:** Section 3.11 — System Architecture / Application Overview  
**Report Page:** Figure 1: SecureShare user authentication interface  
**Mandatory:** YES

**Steps to Capture:**
1. Start the SecureShare application:
   ```cmd
   cd "D:\SSD LAB MIDTERM"
   venv\Scripts\activate
   python run.py
   ```
2. Open browser and navigate to: http://127.0.0.1:5000/auth/login
3. Ensure the login page is fully loaded
4. Capture screenshot showing:
   - Application title "SecureShare"
   - Login form with username/email/password fields
   - Login button
   - Register link
   - Clean browser window (no extra tabs if possible)

**Suggested Filename:** SS-01_Login_Interface.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-02: SecureShare User Dashboard

**Screenshot Title:** SecureShare User Dashboard  
**Report Section:** Section 3.11 — System Architecture / Application Overview  
**Report Page:** Figure 2: SecureShare user dashboard with file management interface  
**Mandatory:** YES

**Steps to Capture:**
1. Login to SecureShare (or register a new user)
2. Navigate to dashboard: http://127.0.0.1:5000/dashboard
3. Ensure dashboard is fully loaded
4. Capture screenshot showing:
   - User greeting (e.g., "Welcome, username")
   - File list table (even if empty)
   - Upload button
   - Navigation menu
   - Logout button

**Suggested Filename:** SS-02_User_Dashboard.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-03: SecureShare File Upload Interface

**Screenshot Title:** SecureShare File Upload Interface  
**Report Section:** Section 3.11 — System Architecture / Application Overview  
**Report Page:** Figure 3: SecureShare file upload interface with validation  
**Mandatory:** YES

**Steps to Capture:**
1. Login to SecureShare
2. Navigate to upload page: http://127.0.0.1:5000/upload
3. Ensure upload form is fully loaded
4. Capture screenshot showing:
   - File input field
   - Description textarea
   - Upload button
   - Allowed file types note (if visible)
   - Cancel/back navigation

**Suggested Filename:** SS-03_File_Upload.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-04: Buffer Overflow Before Fix - AddressSanitizer Output

**Screenshot Title:** Buffer Overflow Before Fix - AddressSanitizer Output  
**Report Section:** Section 8.1 — Buffer Overflow / Reproducible Test Case  
**Report Page:** Figure 8: AddressSanitizer detection of stack buffer overflow in vulnerable implementation  
**Mandatory:** YES

**Steps to Capture:**
1. Open Command Prompt (not PowerShell)
2. Navigate to native module:
   ```cmd
   cd "D:\SSD LAB MIDTERM\native_module"
   ```
3. Compile vulnerable version with ASAN:
   ```cmd
   gcc -Wall -Wextra -g -fsanitize=address -fno-omit-frame-pointer buffer_overflow_demo.c -o buffer_overflow_vulnerable
   ```
4. Run vulnerable version:
   ```cmd
   .\buffer_overflow_vulnerable
   ```
5. Capture terminal output showing:
   - ASAN error message
   - Stack-buffer-overflow detection
   - Line number reference
   - Crash location
   - "ABORTING" message

**Note:** If ASAN is not available on your MinGW installation, compile without ASAN and document that this limitation prevents ASAN evidence capture.

**Suggested Filename:** SS-04_Buffer_Overflow_Before_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-05: Buffer Overflow After Fix - Secure Implementation Output

**Screenshot Title:** Buffer Overflow After Fix - Secure Implementation Output  
**Report Section:** Section 8.1 — Buffer Overflow / Secure Implementation  
**Report Page:** Figure 9: Secure implementation safely rejecting oversized input without memory corruption  
**Mandatory:** YES

**Steps to Capture:**
1. Compile secure version:
   ```cmd
   gcc -Wall -Wextra -g -fstack-protector-strong buffer_overflow_demo.c -o buffer_overflow_secure
   ```
2. Run secure version:
   ```cmd
   .\buffer_overflow_secure
   ```
3. Capture terminal output showing:
   - Error message rejecting oversized input
   - No crash
   - Program continues execution
   - "[SECURE]" messages indicating safe operation

**Suggested Filename:** SS-05_Buffer_Overflow_After_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-06: Command Injection Before Fix - Vulnerable Execution

**Screenshot Title:** Command Injection Before Fix - Vulnerable Execution  
**Report Section:** Section 8.2 — Command Injection / Reproducible Test Case  
**Report Page:** Figure 10: Command injection vulnerability allowing arbitrary command execution  
**Mandatory:** YES

**Steps to Capture:**
1. Navigate to native module:
   ```cmd
   cd "D:\SSD LAB MIDTERM\native_module"
   ```
2. Run command injection demo:
   ```cmd
   python command_injection_demo.py
   ```
3. Capture terminal output showing:
   - Malicious input with semicolon (e.g., "document.txt; echo INJECTED")
   - Output showing injected command executed
   - "⚠️ COMMAND INJECTION SUCCESSFUL" message
   - Vulnerability confirmation

**Note:** On Windows, the injection may not trigger as expected due to shell differences. Document the actual output and explain Windows limitations.

**Suggested Filename:** SS-06_Command_Injection_Before_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-07: Command Injection After Fix - Secure Rejection

**Screenshot Title:** Command Injection After Fix - Secure Rejection  
**Report Section:** Section 8.2 — Command Injection / Secure Implementation  
**Report Page:** Figure 11: Secure implementation rejecting command injection via input validation  
**Mandatory:** YES

**Steps to Capture:**
1. Run command injection demo (same command as SS-06)
2. Capture terminal output showing:
   - Malicious input with semicolon
   - Error message rejecting invalid characters
   - No command execution
   - "✅ INJECTION REJECTED" message
   - Protection working

**Suggested Filename:** SS_07_Command_Injection_After_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-08: IDOR Before Fix - Unauthorized Access Attempt

**Screenshot Title:** IDOR Before Fix - Unauthorized Access Attempt  
**Report Section:** Section 8.3 — IDOR / Reproducible Test Case  
**Report Page:** Figure 12: IDOR protection blocking unauthorized file access  
**Mandatory:** YES

**Steps to Capture:**
1. Start SecureShare application
2. Register user_a and user_b (if not already registered)
3. Login as user_a
4. Upload a file and note the file ID from URL (e.g., /file/1)
5. Logout
6. Login as user_b
7. Try to access user_a's file: http://127.0.0.1:5000/file/1
8. Capture browser showing:
   - Error message "You do not have permission to access this file"
   - URL showing file ID
   - Login status showing user_b
   - Redirect to dashboard

**Suggested Filename:** SS-08_IDOR_Before_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-09: IDOR After Fix - Authorized Access After Sharing

**Screenshot Title:** IDOR After Fix - Authorized Access After Sharing  
**Report Section:** Section 8.3 — IDOR / Reproducible Test Case  
**Report Page:** Figure 13: IDOR protection allowing authorized access after sharing  
**Mandatory:** YES

**Steps to Capture:**
1. Logout as user_b
2. Login as user_a
3. Go to the file page: http://127.0.0.1:5000/file/1
4. Click "Share" and share with user_b
5. Logout
6. Login as user_b
7. Access the file again: http://127.0.0.1:5000/file/1
8. Capture browser showing:
   - File content visible
   - Sharing indicator showing user_b has access
   - No error message
   - Successful file display

**Suggested Filename:** SS-09_IDOR_After_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-10: CSRF Before Fix - Vulnerable Request Execution

**Screenshot Title:** CSRF Before Fix - Vulnerable Request Execution  
**Report Section:** Section 8.4 — CSRF / Reproducible Test Case  
**Report Page:** Figure 14: CSRF vulnerability allowing unauthorized state changes via malicious link  
**Mandatory:** YES

**Steps to Capture:**
1. Navigate to native module:
   ```cmd
   cd "D:\SSD LAB MIDTERM\native_module"
   ```
2. Run CSRF demo:
   ```cmd
   python csrf_demo.py
   ```
3. Open browser to vulnerable app: http://127.0.0.1:5001
4. Click "CLAIM PRIZE" on the attack page
5. Capture browser showing:
   - Malicious link
   - Confirmation that file was deleted
   - No CSRF token error
   - Vulnerability demonstrated

**Suggested Filename:** SS-10_CSRF_Before_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-11: CSRF After Fix - Token Validation Rejection

**Screenshot Title:** CSRF After Fix - Token Validation Rejection  
**Report Section:** Section 8.4 — CSRF / Reproducible Test Case  
**Report Page:** Figure 15: CSRF protection rejecting malicious request with invalid token  
**Mandatory:** YES

**Steps to Capture:**
1. Open browser to secure app: http://127.0.0.1:5002
2. Click "CLAIM PRIZE" on the attack page
3. Capture browser showing:
   - CSRF error message (400 Bad Request)
   - File not deleted
   - Protection working
   - Error details

**Suggested Filename:** SS-11_CSRF_After_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-12: Clickjacking Before Fix - Page Embedded in Iframe

**Screenshot Title:** Clickjacking Before Fix - Page Embedded in Iframe  
**Report Section:** Section 8.5 — Clickjacking / Reproducible Test Case  
**Report Page:** Figure 16: Clickjacking vulnerability allowing page to be embedded in iframe  
**Mandatory:** YES

**Steps to Capture:**
1. Navigate to native module:
   ```cmd
   cd "D:\SSD LAB MIDTERM\native_module"
   ```
2. Run clickjacking demo:
   ```cmd
   python clickjacking_demo.py
   ```
3. Open browser to attacker page: http://127.0.0.1:5003
4. Capture browser showing:
   - Iframe visible with target site loaded
   - No X-Frame-Options error
   - Page successfully embedded
   - Deceptive overlay visible

**Suggested Filename:** SS-12_Clickjacking_Before_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-13: Clickjacking After Fix - Iframe Blocked by Header

**Screenshot Title:** Clickjacking After Fix - Iframe Blocked by Header  
**Report Section:** Section 8.5 — Clickjacking / Reproducible Test Case  
**Report Page:** Figure 17: Clickjacking protection blocking iframe embedding via X-Frame-Options header  
**Mandatory:** YES

**Steps to Capture:**
1. Open browser to attacker page with secure target: http://127.0.0.1:5004
2. Capture browser showing:
   - Browser error message "Refused to display... in a frame because it set 'X-Frame-Options' to 'deny'"
   - Iframe not loaded
   - Empty iframe area
   - Protection working

**Suggested Filename:** SS-13_Clickjacking_After_Fix.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-14: SAST Scan Results - Semgrep Output

**Screenshot Title:** SAST Scan Results - Semgrep Output  
**Report Section:** Section 9.1 — SAST / Actual Findings  
**Report Page:** Figure 18: Semgrep SAST scan results showing 1 WARNING severity finding  
**Mandatory:** YES

**Steps to Capture:**
1. Navigate to project root:
   ```cmd
   cd "D:\SSD LAB MIDTERM"
   ```
2. Run Semgrep scan:
   ```cmd
   semgrep --config .semgrep.yml app/
   ```
3. Capture terminal output showing:
   - Scan summary
   - Finding details (python.debug.enabled)
   - Severity WARNING
   - File path (app/config.py)
   - Line number
   - No HIGH/CRITICAL findings

**Alternative:** The Semgrep results are already available in `pipeline_results/semgrep_results.json`. You can open this file in a text editor and capture a screenshot of the JSON content.

**Suggested Filename:** SS-14_SAST_Results.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-15: DAST Scan Results - OWASP ZAP Report

**Screenshot Title:** DAST Scan Results - OWASP ZAP Report  
**Report Section:** Section 9.2 — DAST / Expected Findings  
**Report Page:** Figure 19: OWASP ZAP DAST scan results showing security controls in place  
**Mandatory:** YES

**Steps to Capture:**
1. Install OWASP ZAP from https://www.zaproxy.org/download/
2. Start SecureShare application
3. Run ZAP baseline scan:
   ```cmd
   zap-cli quick-scan --self-contained http://127.0.0.1:5000
   ```
4. Generate report:
   ```cmd
   zap-cli report -o zap_report.html -f html
   ```
5. Open zap_report.html in browser
6. Capture browser showing:
   - Alert summary table
   - Risk levels
   - Scan statistics
   - No High/Critical alerts (expected)
   - Security controls detected

**Note:** OWASP ZAP installation and execution is required. If ZAP cannot be installed, document this limitation and explain why the screenshot is not available.

**Suggested Filename:** SS-15_DAST_Results.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-16: GitHub Actions Pipeline Success

**Screenshot Title:** GitHub Actions Pipeline Success  
**Report Section:** Section 10.9 — Security Gate Demonstration  
**Report Page:** Figure 20: GitHub Actions CI/CD pipeline showing successful security gate pass  
**Mandatory:** YES

**Steps to Capture:**
1. Push repository to GitHub (if not already pushed)
2. Navigate to GitHub repository
3. Click "Actions" tab
4. Click on the workflow run
5. Capture browser showing:
   - Workflow name (Security CI/CD Pipeline)
   - All jobs passed (security-scan, test, security-gate)
   - Green status indicators
   - Success message
   - Run duration

**Note:** Requires repository to be pushed to GitHub. If not pushed, document this limitation.

**Suggested Filename:** SS-16_GitHub_Actions_Success.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-17: GitHub Actions Pipeline Failure - Security Gate

**Screenshot Title:** GitHub Actions Pipeline Failure - Security Gate  
**Report Section:** Section 10.9 — Security Gate Demonstration  
**Report Page:** Figure 21: GitHub Actions CI/CD pipeline showing security gate failure on vulnerability detection  
**Mandatory:** YES

**Steps to Capture:**
1. Create test branch with intentional vulnerability:
   ```cmd
   git checkout -b test-security-gate-fail
   # Add vulnerable code (e.g., eval(user_input))
   git add .
   git commit -m "Test: Add intentional vulnerability"
   git push origin test-security-gate-fail
   ```
2. Create pull request from test-security-gate-fail to main
3. Navigate to GitHub repository
4. Click "Actions" tab
5. Click on the workflow run
6. Capture browser showing:
   - Workflow name
   - Security-scan job failed
   - Red status indicators
   - Error message showing vulnerability detected
   - Security gate failure

**Note:** Requires repository to be pushed to GitHub and test branch created. If not pushed, document this limitation.

**Suggested Filename:** SS-17_GitHub_Actions_Failure.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-18: Jira Sprint Board

**Screenshot Title:** Jira Sprint Board  
**Report Section:** Section 13.3 — To Do, In Progress and Done Workflow  
**Report Page:** Figure 22: Jira sprint board showing PNE-to-threat-to-fix traceability  
**Mandatory:** YES

**Steps to Capture:**
1. Set up Jira project (if not already set up)
2. Navigate to Jira board
3. Configure sprint board with columns: To Do, In Progress, Done
4. Create issues for PNE, threats, fixes, and tests
5. Link issues to show traceability
6. Capture browser showing:
   - Sprint name
   - Backlog column
   - In-progress column
   - Done column
   - Task cards with status
   - Issue links showing traceability

**Note:** Requires Jira project setup. If Jira is not used, document this limitation and explain alternative tracking method (e.g., GitHub Issues).

**Suggested Filename:** SS-18_Jira_Sprint_Board.png  
**Location:** Save to `reports/final/screenshots/`

---

### SS-19: GitHub Pull Request Review

**Screenshot Title:** GitHub Pull Request Review  
**Report Section:** Section 13.7 — Pull Requests and Peer Reviews  
**Report Page:** Figure 23: GitHub pull request with peer review and CI/CD validation  
**Mandatory:** YES

**Steps to Capture:**
1. Create a feature branch:
   ```cmd
   git checkout -b feature/secure-implementation
   # Make changes
   git add .
   git commit -m "Implement security feature"
   git push origin feature/secure-implementation
   ```
2. Create pull request from feature branch to main
3. Add review comments
4. Request review from team member
5. Wait for CI/CD checks to complete
6. Capture browser showing:
   - PR title
   - Changed files
   - Review comments
   - Approval indicators
   - CI/CD check status (green checks)
   - Merge button

**Note:** Requires repository to be pushed to GitHub and team collaboration. If not applicable, document this limitation.

**Suggested Filename:** SS-19_GitHub_PR_Review.png  
**Location:** Save to `reports/final/screenshots/`

---

## Screenshot Capture Best Practices

1. **Use Full Screen:** Capture the entire window or screen to provide context
2. **High Resolution:** Use the highest resolution available for clarity
3. **Clean Interface:** Close unnecessary tabs and windows
4. **Visible Details:** Ensure all required elements are clearly visible
5. **Consistent Style:** Use the same browser and settings for all screenshots
6. **File Naming:** Use the suggested filenames for consistency
7. **Organization:** Save all screenshots to `reports/final/screenshots/`
7. **File Format:** Use PNG format for lossless quality

---

## Alternative to Jira

If Jira is not available, you can use GitHub Issues for project tracking:

1. Create GitHub Issues for each PNE, threat, and fix
2. Use labels to categorize (PNE, Threat, Fix, Test)
3. Link related issues to show traceability
4. Use projects to create Kanban board
5. Capture screenshot of GitHub Issues board instead of Jira

---

## Screenshot Checklist

Use this checklist to track screenshot capture:

- [ ] SS-01: SecureShare Login Interface
- [ ] SS-02: SecureShare User Dashboard
- [ ] SS-03: SecureShare File Upload Interface
- [ ] SS-04: Buffer Overflow Before Fix
- [ ] SS-05: Buffer Overflow After Fix
- [ ] SS-06: Command Injection Before Fix
- [ ] SS-07: Command Injection After Fix
- [ ] SS-08: IDOR Before Fix
- [ ] SS-09: IDOR After Fix
- [ ] SS-10: CSRF Before Fix
- [ ] SS-11: CSRF After Fix
- [ ] SS-12: Clickjacking Before Fix
- [ ] SS-13: Clickjacking After Fix
- [ ] SS-14: SAST Scan Results
- [ ] SS-15: DAST Scan Results
- [ ] SS-16: GitHub Actions Success
- [ ] SS-17: GitHub Actions Failure
- [ ] SS-18: Jira Sprint Board
- [ ] SS-19: GitHub Pull Request Review

---

**Document Version:** 1.0  
**Last Updated:** October 30, 2026  
**Total Screenshots Required:** 19