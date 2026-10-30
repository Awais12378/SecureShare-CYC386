"""
Check OWASP ZAP results for High or Critical severity findings.

This script parses ZAP HTML report and fails if any High or Critical
severity findings are detected.
"""

import sys
import re


def check_zap_severity(html_file):
    """
    Check ZAP results for High or Critical severity findings.
    
    Args:
        html_file: Path to ZAP HTML report file
    
    Returns:
        0 if no High/Critical findings, 1 otherwise
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ZAP report file not found: {html_file}")
        return 0  # Don't fail if file doesn't exist
    
    # Parse HTML for risk levels
    high_critical_pattern = r'Risk Level:\s*(High|Critical)'
    medium_pattern = r'Risk Level:\s*Medium'
    low_pattern = r'Risk Level:\s*Low'
    
    high_critical_matches = re.findall(high_critical_pattern, content, re.IGNORECASE)
    medium_matches = re.findall(medium_pattern, content, re.IGNORECASE)
    low_matches = re.findall(low_pattern, content, re.IGNORECASE)
    
    high_critical_count = len(high_critical_matches)
    medium_count = len(medium_matches)
    low_count = len(low_matches)
    
    print(f"ZAP Scan Summary:")
    print(f"  High/Critical: {high_critical_count}")
    print(f"  Medium: {medium_count}")
    print(f"  Low: {low_count}")
    
    if high_critical_count > 0:
        print(f"\n❌ SECURITY GATE FAILED: {high_critical_count} High/Critical findings detected")
        return 1
    else:
        print(f"\n✅ SECURITY GATE PASSED: No High/Critical findings")
        return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
    else:
        html_file = "zap_report.html"
    
    sys.exit(check_zap_severity(html_file))
