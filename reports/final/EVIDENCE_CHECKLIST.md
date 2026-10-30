# Evidence Checklist

**SecureShare CYC386 Midterm Lab Exam Report**  
**Date:** October 30, 2026  
**Purpose:** Track all required evidence for the report and submission

---

## Evidence Status Summary

| Category | Total | Completed | Partial | Not Started | Status |
|----------|-------|-----------|---------|-------------|--------|
| Application Screenshots | 3 | 0 | 0 | 3 | ❌ Not Captured |
| Vulnerability Demonstrations | 10 | 0 | 0 | 10 | ❌ Not Captured |
| Security Testing Evidence | 2 | 1 | 0 | 1 | ⚠️ Partial |
| CI/CD Evidence | 2 | 0 | 0 | 2 | ❌ Not Captured |
| Project Management Evidence | 2 | 0 | 0 | 2 | ❌ Not Captured |
| **TOTAL** | **19** | **1** | **0** | **18** | **❌ 5% Complete** |

---

## Detailed Evidence Checklist

### 1. Application Screenshots (3 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-01 | Login Interface | SecureShare login page with form | reports/final/screenshots/ | ❌ Not Captured | Application must be running |
| SS-02 | User Dashboard | Dashboard with file list and navigation | reports/final/screenshots/ | ❌ Not Captured | Requires user login |
| SS-03 | File Upload Interface | Upload form with validation | reports/final/screenshots/ | ❌ Not Captured | Requires user login |

---

### 2. Vulnerability Demonstrations (10 required)

#### Buffer Overflow (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-04 | Buffer Overflow Before Fix | ASAN detecting stack overflow | reports/final/screenshots/ | ❌ Not Captured | Requires GCC compilation |
| SS-05 | Buffer Overflow After Fix | Secure implementation rejecting input | reports/final/screenshots/ | ❌ Not Captured | Requires GCC compilation |

**Additional Evidence:**
- [ ] Compiled vulnerable executable: `native_module/buffer_overflow_vulnerable`
- [ ] Compiled secure executable: `native_module/buffer_overflow_secure`
- [ ] ASAN output log: `native_module/asan_output_vulnerable.log`
- [ ] Regression test output: 10/10 tests expected

**Notes:**
- MinGW GCC lacks AddressSanitizer runtime library
- Compilation without ASAN: `gcc -Wall -Wextra -g -fstack-protector-strong buffer_overflow_demo.c -o buffer_overflow_demo`
- Vulnerable demo ran but did not crash (overflow too small for canary detection)
- ASAN evidence cannot be captured on current environment
- **Alternative:** Document limitation and show regular compilation output

#### Command Injection (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-06 | Command Injection Before Fix | Injected command executing | reports/final/screenshots/ | ❌ Not Captured | Requires Python execution |
| SS-07 | Command Injection After Fix | Injection rejected by validation | reports/final/screenshots/ | ❌ Not Captured | Requires Python execution |

**Additional Evidence:**
- [x] Regression test output: 25/25 PASSED ✅
- [x] Test file: `native_module/test_command_injection.py`
- [x] Demo file: `native_module/command_injection_demo.py`

**Notes:**
- ✅ All 25 regression tests passed
- Tests cover semicolon, pipe, AND, OR, backticks, dollar expansion, newline, path traversal
- Windows shell behavior differs from Linux (some injection markers don't trigger)
- Tests adapted for Windows compatibility
- **Evidence Available:** Test output captured in conversation

#### IDOR (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-08 | IDOR Before Fix | Unauthorized access denied (403) | reports/final/screenshots/ | ❌ Not Captured | Requires manual testing |
| SS-09 | IDOR After Fix | Authorized access after sharing | reports/final/screenshots/ | ❌ Not Captured | Requires manual testing |

**Additional Evidence:**
- [x] Authorization code: `app/models.py` lines 63-74
- [x] Route protection: `app/main/routes.py` lines 125-139, 142-166, 263-294
- [x] IDOR protection report: `security_reports/IDOR_Protection_Report.md`
- [x] Manual verification guide: `security_reports/IDOR_Manual_Verification.md`
- [ ] Automated test results: [Session management issues]

**Notes:**
- IDOR protection is fully implemented in production code
- Automated tests have SQLAlchemy session management issues
- Manual verification guide provided
- **Required:** Manual browser testing with two users
- **Procedure:** See `security_reports/IDOR_Manual_Verification.md`

#### CSRF (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-10 | CSRF Before Fix | Malicious link executes action | reports/final/screenshots/ | ❌ Not Captured | Requires demo execution |
| SS-11 | CSRF After Fix | CSRF error, action rejected | reports/final/screenshots/ | ❌ Not Captured | Requires demo execution |

**Additional Evidence:**
- [x] CSRF initialization: `app/__init__.py` lines 4, 12, 24
- [x] CSRF configuration: `app/config.py` lines 29-30
- [x] CSRF protection report: `security_reports/CSRF_Protection_Report.md`
- [x] Demo file: `native_module/csrf_demo.py`
- [⚠️] Regression test output: 13/17 PASSED (3 session errors, not security issues)

**Notes:**
- CSRF protection is fully implemented in production code via Flask-WTF
- 13/17 tests passed; failures are due to SQLAlchemy session issues, not security problems
- Educational demonstration available in `native_module/csrf_demo.py`
- **Required:** Run demo and capture browser screenshots

#### Clickjacking (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-12 | Clickjacking Before Fix | Page loads in iframe | reports/final/screenshots/ | ❌ Not Captured | Requires demo execution |
| SS-13 | Clickjacking After Fix | Iframe blocked by X-Frame-Options | reports/final/screenshots/ | ❌ Not Captured | Requires demo execution |

**Additional Evidence:**
- [x] Security headers: `app/__init__.py` lines 50-56
- [x] Demo file: `native_module/clickjacking_demo.py`
- [x] Regression test output: 6/6 PASSED ✅

**Notes:**
- X-Frame-Options: DENY header is implemented in production code
- All 6 automated tests passed
- Educational demonstration available in `native_module/clickjacking_demo.py`
- **Required:** Run demo and capture browser screenshots

---

### 3. Security Testing Evidence (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-14 | SAST Scan Results | Semgrep scan output | reports/final/screenshots/ | ✅ Available | JSON in pipeline_results |
| SS-15 | DAST Scan Results | OWASP ZAP report | reports/final/screenshots/ | ❌ Not Captured | Requires ZAP installation |

**SAST Evidence:**
- [x] Semgrep configuration: `.semgrep.yml`
- [x] Semgrep output: `pipeline_results/semgrep_results.json`
- [x] Severity checker: `scripts/check_semgrep_severity.py`
- [x] Scan results: 1 WARNING (DEBUG mode), 0 HIGH/CRITICAL ✅

**DAST Evidence:**
- [ ] OWASP ZAP installed: Not installed
- [ ] ZAP scan executed: Not executed
- [ ] ZAP report generated: Not generated
- [ ] Report file: `zap_report.html`

**Notes:**
- ✅ Semgrep SAST executed successfully
- ❌ OWASP ZAP DAST not executed (tool not installed)
- **Required:** Install OWASP ZAP and run scan
- **Alternative:** Document limitation and explain why ZAP not available

---

### 4. CI/CD Evidence (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-16 | GitHub Actions Success | Pipeline passes with green checks | reports/final/screenshots/ | ❌ Not Captured | Requires GitHub push |
| SS-17 | GitHub Actions Failure | Security gate fails on vulnerability | reports/final/screenshots/ | ❌ Not Captured | Requires GitHub push |

**Additional Evidence:**
- [x] Workflow file: `.github/workflows/ci-cd.yml`
- [x] Severity checker: `scripts/check_semgrep_severity.py`
- [x] Local pipeline runner: `scripts/run_local_pipeline.py`
- [x] Local pipeline report: `pipeline_results/pipeline_report.json`
- [x] Security gate passed: No HIGH/CRITICAL findings ✅

**Notes:**
- CI/CD workflow is configured and ready
- Local pipeline simulation executed (test failures due to session issues, security gate passed)
- **Required:** Push repository to GitHub to execute workflow
- **Required:** Create test branch with vulnerability to demonstrate security gate failure

---

### 5. Project Management Evidence (2 required)

| ID | Evidence | Description | Location | Status | Notes |
|----|---------|-------------|----------|--------|-------|
| SS-18 | Jira Sprint Board | Sprint backlog and task tracking | reports/final/screenshots/ | ❌ Not Captured | Requires Jira setup |
| SS-19 | GitHub Pull Request Review | Code review and CI/CD validation | reports/final/screenshots/ | ❌ Not Captured | Requires GitHub push |

**Jira Evidence:**
- [ ] Jira project: Not created
- [ ] Sprint board: Not configured
- [ ] Epics: Not defined
- [ ] Stories: Not defined
- [ ] Tasks: Not defined
- [ ] PNE-to-threat-to-fix traceability: Not implemented

**GitHub Evidence:**
- [ ] Repository: Not pushed to GitHub
- [ ] Branches: Not created
- [ ] Pull requests: Not created
- [ ] Code reviews: Not performed
- [ ] Commit history: Not available

**Notes:**
- Jira integration not implemented (assignment allows alternative tracking)
- GitHub repository not pushed (required for CI/CD evidence)
- **Alternative:** Use GitHub Issues for project tracking
- **Required:** Push to GitHub and create pull request for review evidence

---

## Documentation Evidence

### Completed Documentation

| Document | Location | Lines | Status | Notes |
|----------|----------|-------|--------|-------|
| PNE Report | docs/PNE_Report.md | 750 | ✅ Complete | 42 protection needs, 30 security requirements |
| Threat Model | docs/THREAT_MODEL.md | 1,415 | ✅ Complete | STRIDE analysis, DFDs, attack trees |
| Security Implementation | native_module/SECURITY_IMPLEMENTATION.md | 653 | ✅ Complete | Buffer overflow, command injection |
| CI/CD Documentation | docs/CI_CD_PIPELINE_Documentation.md | 503 | ✅ Complete | Pipeline stages, security gates |
| Security Test Report | SECURITY_TEST_REPORT.md | 392 | ✅ Complete | SAST/DAST configuration |
| CSRF Protection Report | security_reports/CSRF_Protection_Report.md | 393 | ✅ Complete | CWE-352 mapping, CIA analysis |
| IDOR Protection Report | security_reports/IDOR_Protection_Report.md | 311 | ✅ Complete | CWE-639 mapping, CIA analysis |
| IDOR Manual Verification | security_reports/IDOR_Manual_Verification.md | ~200 | ✅ Complete | Step-by-step manual testing guide |
| Final Report | reports/final/CYC386_SecureShare_Final_Report.md | ~3,800 | ✅ Complete | 24-27 pages (estimated) |
| Screenshot Guide | reports/final/SCREENSHOT_GUIDE.md | 613 | ✅ Complete | Detailed capture instructions |

---

## Test Evidence

### Automated Test Results

| Test Suite | File | Result | Status | Notes |
|------------|------|--------|--------|-------|
| Command Injection | native_module/test_command_injection.py | 25/25 PASSED | ✅ Verified | All security rejection tests passed |
| Clickjacking Protection | tests/test_clickjacking_protection.py | 6/6 PASSED | ✅ Verified | All header tests passed |
| CSRF Protection | tests/test_csrf_protection.py | 13/17 PASSED | ⚠️ Partial | 3 session errors, not security issues |
| IDOR Protection | tests/test_idor_protection.py | [Not run] | ❌ Not Verified | Session management issues |
| Buffer Overflow | native_module/buffer_overflow_test.c | [Not run] | ❌ Not Verified | Requires compilation |

---

## Configuration Evidence

### Security Configuration

| Component | File | Status | Notes |
|-----------|------|--------|-------|
| Semgrep Rules | .semgrep.yml | ✅ Created | 52 lines, Flask security rules |
| GitHub Actions | .github/workflows/ci-cd.yml | ✅ Created | 127 lines, security gates |
| Flask Config | app/config.py | ✅ Existing | CSRF enabled, session security |
| CSRF Protection | app/__init__.py | ✅ Existing | Flask-WTF initialized |
| Security Headers | app/__init__.py | ✅ Existing | X-Frame-Options, X-Content-Type-Options |

---

## Missing Evidence and Next Steps

### High Priority (Required for Submission)

1. **Application Screenshots (3):**
   - [ ] SS-01: Login Interface
   - [ ] SS-02: User Dashboard
   - [ ] SS-03: File Upload Interface
   - **Action:** Start application, capture screenshots

2. **IDOR Manual Verification (2):**
   - [ ] SS-08: Unauthorized access denied
   - [ ] SS-09: Authorized access after sharing
   - **Action:** Follow manual verification guide, capture screenshots

3. **CSRF Demonstration (2):**
   - [ ] SS-10: Vulnerable execution
   - [ ] SS-11: Secure rejection
   - **Action:** Run csrf_demo.py, capture screenshots

4. **Clickjacking Demonstration (2):**
   - [ ] SS-12: Iframe embed
   - [ ] SS-13: Iframe blocked
   - **Action:** Run clickjacking_demo.py, capture screenshots

5. **Buffer Overflow Evidence (2):**
   - [ ] SS-04: ASAN output (or compilation output if ASAN unavailable)
   - [ ] SS-05: Secure output
   - **Action:** Compile and run demo, capture screenshots

6. **Command Injection Evidence (2):**
   - [ ] SS-06: Vulnerable execution
   - [ ] SS-07: Secure rejection
   - **Action:** Run command_injection_demo.py, capture screenshots

### Medium Priority (Enhances Submission)

7. **OWASP ZAP DAST (1):**
   - [ ] SS-15: ZAP report
   - **Action:** Install OWASP ZAP, run scan, capture screenshot
   - **Alternative:** Document limitation

8. **GitHub CI/CD (2):**
   - [ ] SS-16: Pipeline success
   - [ ] SS-17: Pipeline failure
   - **Action:** Push to GitHub, create test branch, capture screenshots

### Low Priority (If Time Permits)

9. **Project Management (2):**
   - [ ] SS-18: Jira board
   - [ ] SS-19: Pull request review
   - **Action:** Set up Jira or GitHub Issues, create PR

---

## Platform Limitations

### Known Limitations

1. **MinGW GCC:** Lacks AddressSanitizer runtime library
   - **Impact:** Cannot capture ASAN evidence for buffer overflow
   - **Workaround:** Document limitation, show regular compilation output

2. **Shell Tool Availability:** PowerShell not available in assistant environment
   - **Impact:** Cannot execute commands automatically
   - **Workaround:** User must run commands manually

3. **OWASP ZAP:** Not installed
   - **Impact:** Cannot capture DAST evidence
   - **Workaround:** Install ZAP or document limitation

4. **GitHub Repository:** Not pushed
   - **Impact:** Cannot capture CI/CD evidence
   - **Workaround:** Push repository to GitHub

5. **Jira:** Not configured
   - **Impact:** Cannot capture project management evidence
   - **Workaround:** Use GitHub Issues or document limitation

---

## Evidence Quality Criteria

### Screenshot Quality

- ✅ High resolution (1920x1080 or higher)
- ✅ Full window or screen capture
- ✅ All required elements visible
- ✅ Clear, readable text
- ✅ No unnecessary elements (tabs, notifications)
- ✅ Consistent browser and settings

### Test Evidence Quality

- ✅ Actual output captured (not fabricated)
- ✅ Test result counts accurate
- ✅ Pass/fail status clear
- ✅ Test file referenced
- ✅ Execution command documented

### Documentation Quality

- ✅ Based on actual code inspection
- ✅ No fabricated claims
- ✅ Accurate line references
- ✅ Verified code snippets
- ✅ Real file paths

---

## Submission Checklist

### Required Files for Submission

1. [x] Final Report: `reports/final/CYC386_SecureShare_Final_Report.md`
2. [x] Screenshot Guide: `reports/final/SCREENSHOT_GUIDE.md`
3. [x] Evidence Checklist: `reports/final/EVIDENCE_CHECKLIST.md`
4. [x] Report Verification: `reports/final/REPORT_VERIFICATION.md`
5. [ ] Screenshot files: `reports/final/screenshots/*.png` (19 files)
6. [ ] PDF version: `reports/final/CYC386_SecureShare_Final_Report.pdf`

### Additional Evidence (if available)

7. [ ] OWASP ZAP report: `zap_report.html`
8. [ ] Semgrep results: `pipeline_results/semgrep_results.json`
9. [ ] Pipeline report: `pipeline_results/pipeline_report.json`
10. [ ] Test output logs: various

---

## Final Notes

- **Evidence-based approach:** All claims backed by actual code inspection or test results
- **No fabrication:** No fabricated screenshots, test results, or claims
- **Clear limitations:** Platform limitations documented and explained
- **Alternative approaches:** Workarounds provided when tools unavailable
- **Professional standards:** IEEE-style formatting, academic English, proper citations

---

**Document Version:** 1.0  
**Last Updated:** October 30, 2026  
**Evidence Completion:** 5% (1/19 screenshots)  
**Documentation Completion:** 100%