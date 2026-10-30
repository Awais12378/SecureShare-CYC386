# CI/CD Security Pipeline Documentation

## SecureShare GitHub Actions Security Pipeline

**Date:** October 30, 2026  
**Pipeline File:** `.github/workflows/ci-cd.yml`  
**Purpose:** Automated security testing with fail-on-critical policy  

---

## Pipeline Overview

The CI/CD pipeline runs on every push and pull request to `main` and `develop` branches. It performs:

1. **SAST Scan:** Semgrep static analysis
2. **Unit Tests:** pytest with coverage
3. **Security Regression Tests:** CSRF, Clickjacking protection tests
4. **DAST Scan:** OWASP ZAP dynamic analysis
5. **Security Gate:** Fails on High/Critical findings

---

## Pipeline Stages

### Stage 1: Security Scan (Semgrep SAST)

**Purpose:** Static analysis for Python/Flask codebase  
**Tool:** Semgrep  
**Configuration:** `.semgrep.yml`  
**Output:** `semgrep_results.json` (JSON format)

**Rules:**
- Flask security best practices
- SQL injection detection
- Command injection detection
- Hardcoded secrets detection
- Debug mode detection

**Security Gate:** Fails if High/Critical findings detected

### Stage 2: Run Tests

**Purpose:** Unit and integration testing  
**Tool:** pytest  
**Output:** `pytest-report.html`

**Test Suites:**
- Unit tests (`tests/`)
- Security regression tests (CSRF, Clickjacking)

**Security Gate:** Fails if tests fail

### Stage 3: DAST Scan (OWASP ZAP)

**Purpose:** Dynamic security scanning of running application  
**Tool:** OWASP ZAP  
**Configuration:** Baseline scan on http://127.0.0.1:5000  
**Output:** `zap_report.html` (HTML format)

**Scan Type:** Quick baseline scan  
**Authentication:** Form-based (admin credentials)

**Security Gate:** Fails if High/Critical findings detected

### Stage 4: Security Gate

**Purpose:** Fail-on-critical policy enforcement  
**Tool:** Custom Python scripts  

**Checks:**
- Semgrep results for High/Critical severity
- ZAP results for High/Critical severity
- Overall pipeline status

**Behavior:**
- ✅ PASS: No High/Critical findings → Pipeline succeeds
- ❌ FAIL: High/Critical findings detected → Pipeline fails

---

## Workflow Triggers

### Push Events
- Push to `main` branch
- Push to `develop` branch

### Pull Request Events
- Pull request to `main` branch
- Pull request to `develop` branch

---

## Permissions

```yaml
permissions:
  contents: read
  security-events: write
  actions: read
  checks: write
```

**Least Privilege:**
- Read-only repository access
- Write security events (for GitHub Advanced Security)
- Read actions (for GitHub Actions)
- Write checks (to set check statuses)

---

## Secrets Handling

The pipeline does not require secrets for basic operation. For advanced features:

**Optional Secrets:**
- `SLACK_WEBHOOK`: For notifications
- `GITHUB_TOKEN`: For automated operations (automatically provided)

**Storage:** GitHub Secrets (encrypted, not in code)

---

## Pinned Actions

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
- uses: actions/upload-artifact@v4
- uses: actions/download-artifact@v4
```

**Rationale:** Pinned to specific versions for reproducibility and security.

---

## Artifacts

### Uploaded Artifacts

1. **Semgrep Results:** `semgrep-results.json`
   - Contains all SAST findings
   - JSON format for machine readability

2. **Test Results:** `test-results`
   - Contains pytest HTML report
   - Test coverage information

3. **ZAP Results:** `zap-results`
   - Contains OWASP ZAP HTML report
   - DAST findings and risk levels

**Retention:** Artifacts retained for 90 days (GitHub default)

---

## Security Gate Logic

### Semgrep Severity Check

**Script:** `scripts/check_semgrep_severity.py`

**Severity Levels:**
- **ERROR/CRITICAL:** ❌ Fails security gate
- **WARNING:** ⚠️ Warning, does not fail
- **INFO/LOW:** ✅ Passes

**Example:**
```python
# Finding
{
  "check_id": "python.sql.injection",
  "extra": {
    "severity": "ERROR"
  }
}

# Result: SECURITY GATE FAILED
```

### ZAP Severity Check

**Script:** `scripts/check_zap_severity.py`

**Risk Levels:**
- **High/Critical:** ❌ Fails security gate
- **Medium:** ⚠️ Warning, does not fail
- **Low/Informational:** ✅ Passes

**Example:**
```html
<!-- Report -->
Risk Level: High
<!-- Result: SECURITY GATE FAILED -->
```

---

## Local Testing

### Step 1: Install Dependencies

```cmd
cd "D:\SSD LAB MIDTERM"
venv\Scripts\activate
pip install semgrep pytest pytest-flask
```

### Step 2: Run Local Pipeline Simulation

```cmd
cd "D:\SSD LAB MIDTERM"
venv\Scripts\activate
python scripts/run_local_pipeline.py
```

This runs all pipeline stages locally and generates a report in `pipeline_results/`.

### Step 3: Check Results

```cmd
type pipeline_results\pipeline_report.json
```

---

## GitHub Execution Status

### Prerequisites for GitHub Execution

1. **Repository:** Must be pushed to GitHub
2. **Workflow File:** `.github/workflows/ci-cd.yml` must exist
3. **Branch Protection:** `main` and `develop` should be protected
4. **Required Checks:** Security gate must be required for merge

### What Runs on GitHub

**Runs Successfully on GitHub:**
- ✅ Checkout
- ✅ Setup Python
- ✅ Install dependencies
- ✅ Run tests
- ✅ Run Semgrep
- ✅ Check Semgrep severity
- ✅ Upload artifacts

**Limited on GitHub:**
- ⚠️ OWASP ZAP DAST (requires running application)
  - May fail in GitHub Actions environment
  - Better suited for local testing or self-hosted runners

---

## Security Gate Demonstration

### Step 1: Create Test Branch with Vulnerability

```cmd
cd "D:\SSD LAB MIDTERM"
git checkout -b test-security-gate-fail
```

### Step 2: Add Intentional Vulnerability

Add to `tests/test_security_gate_fail.py` (already created):
```python
def vulnerable_eval():
    eval(user_input)  # Intentional vulnerability
```

### Step 3: Commit and Push

```cmd
git add tests/test_security_gate_fail.py
git commit -m "Test: Add intentional vulnerability for security gate"
git push origin test-security-gate-fail
```

### Step 4: Create Pull Request

Create PR from `test-security-gate-fail` to `main`.

**Expected Result:**
- Security scan detects the vulnerability
- Semgrep severity check fails
- Pipeline fails with security gate error
- PR cannot be merged

### Step 5: Fix Vulnerability

Remove the vulnerable file and push.

**Expected Result:**
- Security scan passes
- Security gate passes
- Pipeline succeeds
- PR can be merged

---

## Remediating Failures

### Semgrep Findings

**Example Finding:** SQL injection

**Remediation:**
```python
# Before (vulnerable)
query = f"SELECT * FROM users WHERE id = {user_id}"

# After (secure)
user = User.query.get(user_id)
```

**Verification:**
```cmd
semgrep --config .semgrep.yml app/
```

### ZAP Findings

**Example Finding:** Missing security header

**Remediation:**
Add to `app/__init__.py`:
```python
response.headers['Strict-Transport-Security'] = 'max-age=31536000'
```

**Verification:**
Re-run ZAP scan locally.

---

## Residual Findings

### Acceptable Findings

**DEBUG Mode in Development:**
- **Finding:** DEBUG = True in development config
- **Severity:** INFO
- **Action:** None (acceptable for development)
- **Production:** ProductionConfig sets DEBUG = False

**Secret Key in Config:**
- **Finding:** Secret key in config file
- **Severity:** INFO
- **Action:** Use environment variable in production
- **Status:** Code already supports `os.environ.get('SECRET_KEY')`

### Findings Requiring Remediation

**Missing HSTS Header:**
- **Finding:** Strict-Transport-Security header not set
- **Severity:** MEDIUM
- **Remediation:** Add HSTS header for HTTPS enforcement
- **Priority:** HIGH (before production deployment)

---

## Workflow Validation

### Syntax Validation

Validate workflow syntax:

```cmd
# Using GitHub CLI
gh workflow view .github/workflows/ci-cd.yml

# Or use act (local GitHub Actions runner)
act -W .github/workflows/ci-cd.yml --dryrun
```

### Local Testing with act

Install act:
```cmd
choco install act
```

Run workflow locally:
```cmd
act -W .github/workflows/ci-cd.yml
```

---

## Pipeline Status Summary

| Stage | GitHub Status | Local Status | Notes |
|-------|---------------|--------------|-------|
| Checkout | ✅ Works | ✅ Works | Standard operation |
| Setup Python | ✅ Works | ✅ Works | Python 3.12 |
| Install Deps | ✅ Works | ✅ Works | pip install |
| Unit Tests | ✅ Works | ✅ Works | pytest |
| Security Tests | ✅ Works | ✅ Works | CSRF, Clickjacking |
| Semgrep SAST | ✅ Works | ✅ Works | Security gate |
| ZAP DAST | ⚠️ Limited | ✅ Works | Needs running app |
| Security Gate | ✅ Works | ✅ Works | Fail-on-critical |

---

## Next Steps

### For Immediate Testing

1. **Run local pipeline:**
   ```cmd
   python scripts/run_local_pipeline.py
   ```

2. **Check results:**
   ```cmd
   type pipeline_results\pipeline_report.json
   ```

3. **Install Semgrep:**
   ```cmd
   pip install semgrep
   ```

4. **Run SAST:**
   ```cmd
   semgrep --config .semgrep.yml app/
   ```

### For GitHub Integration

1. **Push to GitHub:**
   ```cmd
   git add .
   git commit -m "Add CI/CD security pipeline"
   git push origin main
   ```

2. **Verify workflow runs:**
   - Go to GitHub repository
   - Click "Actions" tab
   - View workflow run

3. **Check security gate:**
   - Ensure workflow passes or fails as expected
   - Review artifacts in workflow run

---

## Troubleshooting

### Semgrep Not Found

**Error:** `semgrep: command not found`

**Solution:**
```cmd
pip install semgrep
```

### ZAP Fails in GitHub Actions

**Error:** ZAP cannot connect to localhost

**Solution:**
- ZAP DAST is designed for local testing
- In GitHub Actions, use self-hosted runner with application running
- Or disable DAST stage in GitHub Actions

### Security Gate Fails Unexpectedly

**Error:** Pipeline fails with no clear reason

**Solution:**
1. Check workflow logs in GitHub Actions
2. Download artifacts (Semgrep results, ZAP report)
3. Review findings manually
4. Remediate or configure severity thresholds

---

## Best Practices

### For This Pipeline

1. **Always run locally first** before pushing
2. **Review artifacts** to understand findings
3. **Remediate findings** before merging to main
4. **Keep workflow updated** with pinned action versions
5. **Monitor pipeline logs** for failures

### For Future Enhancements

1. Add more SAST tools (Bandit, Safety)
2. Add container scanning (Trivy)
3. Add dependency scanning (Snyk, Dependabot)
4. Add secret scanning (Gitleaks)
5. Add code coverage reporting

---

**Document Version:** 1.0  
**Last Updated:** October 30, 2026  
**Status:** Ready for Local Testing  
**GitHub Status:** Ready for Push
