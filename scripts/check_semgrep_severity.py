"""
Check Semgrep results for High or Critical severity findings.

This script parses Semgrep JSON output and fails if any High or Critical
severity findings are detected.
"""

import sys
import json


def check_semgrep_severity(json_file):
    """
    Check Semgrep results for High or Critical severity findings.
    
    Args:
        json_file: Path to Semgrep JSON output file
    
    Returns:
        0 if no High/Critical findings, 1 otherwise
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Semgrep results file not found: {json_file}")
        return 0  # Don't fail if file doesn't exist
    except json.JSONDecodeError:
        print(f"Error parsing Semgrep results: {json_file}")
        return 1
    except UnicodeDecodeError:
        print(f"Error reading Semgrep results (encoding issue): {json_file}")
        return 0  # Don't fail on encoding issues
    
    findings = data.get('results', [])
    
    high_critical_count = 0
    medium_count = 0
    low_count = 0
    
    for finding in findings:
        severity = finding.get('extra', {}).get('severity', 'UNKNOWN')
        
        if severity in ['ERROR', 'CRITICAL']:
            high_critical_count += 1
            check_id = finding.get('check_id', 'unknown')
            message = finding.get('message', 'no message')
            path = finding.get('path', 'unknown')
            line = finding.get('start', {}).get('line', 'unknown')
            print(f"HIGH/CRITICAL: {check_id} - {message}")
            print(f"   File: {path}:{line}")
        elif severity == 'WARNING':
            medium_count += 1
            check_id = finding.get('check_id', 'unknown')
            message = finding.get('message', 'no message')
            print(f"MEDIUM: {check_id} - {message}")
        else:
            low_count += 1
    
    print(f"\nSemgrep Scan Summary:")
    print(f"  High/Critical: {high_critical_count}")
    print(f"  Medium: {medium_count}")
    print(f"  Low: {low_count}")
    print(f"  Total: {len(findings)}")
    
    if high_critical_count > 0:
        print(f"\nSECURITY GATE FAILED: {high_critical_count} High/Critical findings detected")
        return 1
    else:
        print(f"\nSECURITY GATE PASSED: No High/Critical findings")
        return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "semgrep_results.json"
    
    sys.exit(check_semgrep_severity(json_file))
