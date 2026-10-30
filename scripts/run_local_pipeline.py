#!/usr/bin/env python
"""
Local CI/CD Security Pipeline Simulation

This script simulates the GitHub Actions CI/CD pipeline locally for testing
and demonstration purposes. It runs the same checks that would run in GitHub Actions.
"""

import subprocess
import sys
import os
import json
from datetime import datetime


def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*70}")
    print(f"STAGE: {description}")
    print(f"{'='*70}")
    print(f"Command: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    print(f"Exit Code: {result.returncode}")
    if result.stdout:
        print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
    
    return result.returncode == 0


def main():
    print("="*70)
    print("SECURESHARE CI/CD SECURITY PIPELINE (LOCAL SIMULATION)")
    print("="*70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create results directory
    os.makedirs('pipeline_results', exist_ok=True)
    
    results = {}
    
    # Stage 1: Checkout (simulated)
    results['checkout'] = run_command("git status", "Checkout Repository")
    
    # Stage 2: Setup Python
    results['setup'] = run_command("python --version", "Setup Python")
    
    # Stage 3: Install Dependencies
    results['install'] = run_command(
        "pip install -q -r requirements.txt",
        "Install Dependencies"
    )
    
    # Stage 4: Run Unit Tests
    results['unit_tests'] = run_command(
        "python -m pytest tests/ -v --tb=short",
        "Run Unit Tests"
    )
    
    # Stage 5: Run Security Regression Tests
    results['security_tests'] = run_command(
        "python -m pytest tests/test_csrf_protection.py tests/test_clickjacking_protection.py -v",
        "Run Security Regression Tests"
    )
    
    # Stage 6: Run Semgrep SAST
    results['sast'] = run_command(
        "semgrep --config .semgrep.yml --json --output pipeline_results/semgrep_results.json app/",
        "Run Semgrep SAST"
    )
    
    # Stage 7: Check Semgrep Severity
    results['sast_check'] = run_command(
        "python scripts/check_semgrep_severity.py pipeline_results/semgrep_results.json",
        "Check Semgrep Severity (Security Gate)"
    )
    
    # Stage 8: Generate Report
    print(f"\n{'='*70}")
    print("STAGE: Generate Pipeline Report")
    print(f"{'='*70}")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'stages': results,
        'overall_status': 'PASS' if all(results.values()) else 'FAIL'
    }
    
    with open('pipeline_results/pipeline_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("Pipeline report saved to: pipeline_results/pipeline_report.json")
    
    # Final Summary
    print(f"\n{'='*70}")
    print("PIPELINE SUMMARY")
    print(f"{'='*70}")
    
    for stage, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{stage:20s}: {status}")
    
    print(f"\nOverall Status: {report['overall_status']}")
    
    if report['overall_status'] == 'FAIL':
        print("\n❌ SECURITY GATE FAILED - Pipeline failed")
        return 1
    else:
        print("\n✅ SECURITY GATE PASSED - Pipeline succeeded")
        return 0


if __name__ == "__main__":
    sys.exit(main())
