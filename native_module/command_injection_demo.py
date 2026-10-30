"""
COMMAND INJECTION DEMONSTRATION MODULE

PURPOSE: Educational demonstration of command injection vulnerability
         in a file metadata processing context (simulating SecureShare functionality)

WARNING: This code contains INTENTIONAL VULNERABILITIES for educational
         purposes only. DO NOT use in production or integrate with the
         main SecureShare application.

CWE: CWE-78 (OS Command Injection)
OWASP: A03:2021 - Injection

SCENARIO: A file metadata processor that calls external system commands
            to analyze file properties (simulating real-world use cases
            like file type detection, image processing, or file conversion)
"""

import subprocess
import os
import sys
from typing import Tuple, Optional

# ============================================================
# VULNERABLE IMPLEMENTATION
# ============================================================

def get_file_metadata_vulnerable(filename: str) -> Tuple[str, str, str]:
    """
    VULNERABLE: Extract file metadata using shell command
    
    VULNERABILITY: Uses shell=True and interpolates user input directly
    into command string. This allows command injection via shell metacharacters.
    
    SHELL METACHARACTERS THAT CAN BE INJECTED:
    - ; (command separator)
    - | (pipe)
    - && (AND operator)
    - || (OR operator)
    - ` (command substitution)
    - $ (variable expansion)
    - \n (newline separator)
    - $(...) (modern command substitution)
    
    REALISTIC SCENARIO: Many applications use external tools like:
    - file command (file type detection)
    - exiftool (metadata extraction)
    - ImageMagick (image processing)
    - ffmpeg (video conversion)
    
    Args:
        filename: User-controlled filename (UNTRUSTED INPUT)
        
    Returns:
        Tuple of (file_type, file_size, permissions)
    """
    # VULNERABLE: Direct string interpolation with shell=True
    # Attacker can inject: filename.txt; rm -rf / ; echo
    command = f"file {filename}"
    
    try:
        # VULNERABLE: shell=True enables shell interpretation
        result = subprocess.run(
            command,
            shell=True,  # <-- VULNERABILITY: Shell interpretation enabled
            capture_output=True,
            text=True,
            timeout=5
        )
        
        output = result.stdout.strip()
        return output, "vulnerable_size", "vulnerable_perms"
        
    except subprocess.TimeoutExpired:
        return "timeout", "vulnerable_size", "vulnerable_perms"
    except Exception as e:
        return f"error: {e}", "vulnerable_size", "vulnerable_perms"


def process_file_vulnerable(filepath: str, operation: str) -> str:
    """
    VULNERABLE: Process file with user-controlled operation
    
    VULNERABILITY: Operation parameter is interpolated into command
    without validation. Can inject arbitrary commands.
    
    REALISTIC SCENARIO: File processors that accept operation types
    like "analyze", "convert", "compress", "extract"
    
    Args:
        filepath: User-controlled file path
        operation: User-controlled operation type (UNTRUSTED INPUT)
        
    Returns:
        Command output
    """
    # VULNERABLE: Operation and filepath both interpolated
    # Attacker can inject: filepath && malicious_command
    command = f"echo Processing {operation} on {filepath}"
    
    try:
        result = subprocess.run(
            command,
            shell=True,  # <-- VULNERABILITY
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return result.stdout.strip()
        
    except Exception as e:
        return f"error: {e}"


# ============================================================
# SECURE IMPLEMENTATION
# ============================================================

def get_file_metadata_secure(filename: str) -> Tuple[str, str, str]:
    """
    SECURE: Extract file metadata using safe subprocess call
    
    SECURITY CONTROLS:
    1. Input validation (filename sanitization)
    2. Shell disabled (shell=False)
    3. Argument array (no string interpolation)
    4. Allow-list validation for operations
    5. Error handling
    
    Args:
        filename: User-controlled filename (UNTRUSTED INPUT)
        
    Returns:
        Tuple of (file_type, file_size, permissions) or error message
    """
    # Security Control 1: Input validation
    if not filename or not isinstance(filename, str):
        return "error: invalid filename", "", ""
    
    # Security Control 2: Sanitize filename (remove dangerous characters)
    # Allow only alphanumeric, underscores, hyphens, dots
    import re
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        return "error: filename contains invalid characters", "", ""
    
    # Security Control 3: Check file exists and is in allowed directory
    # (In real app, validate against allowed upload directory)
    # For demo, we just validate the filename format
    
    # Security Control 4: Use argument array instead of string interpolation
    # Security Control 5: Disable shell interpretation
    try:
        # For demonstration, we use 'echo' as a safe command
        # In real app, this would be the actual file analysis tool
        result = subprocess.run(
            ['echo', f"metadata_{filename}"],  # Argument array
            shell=False,  # <-- SECURITY: Shell interpretation disabled
            capture_output=True,
            text=True,
            timeout=5
        )
        
        output = result.stdout.strip()
        
        # Simulate getting real metadata
        file_size = "1024 bytes"
        permissions = "rw-r--r--"
        
        return output, file_size, permissions
        
    except subprocess.TimeoutExpired:
        return "error: timeout", "", ""
    except FileNotFoundError:
        return "error: command not found", "", ""
    except Exception as e:
        return f"error: {e}", "", ""


def process_file_secure(filepath: str, operation: str) -> str:
    """
    SECURE: Process file with safe subprocess call
    
    SECURITY CONTROLS:
    1. Input validation for both filepath and operation
    2. Operation allow-list
    3. Shell disabled
    4. Argument array
    5. Path validation
    
    Args:
        filepath: User-controlled file path
        operation: User-controlled operation type
        
    Returns:
        Command output or error message
    """
    # Security Control 1: Input validation
    if not filepath or not operation:
        return "error: missing parameters"
    
    # Security Control 2: Operation allow-list
    ALLOWED_OPERATIONS = {'analyze', 'info', 'check', 'validate'}
    if operation not in ALLOWED_OPERATIONS:
        return f"error: operation '{operation}' not allowed"
    
    # Security Control 3: Path validation
    # Remove path traversal attempts
    if '..' in filepath or filepath.startswith('/'):
        return "error: invalid path"
    
    # Security Control 4: Allow only safe filename characters
    import re
    basename = os.path.basename(filepath)
    if not re.match(r'^[a-zA-Z0-9._-]+$', basename):
        return "error: filename contains invalid characters"
    
    # Security Control 5: Use argument array with shell=False
    try:
        result = subprocess.run(
            ['echo', f"{operation}_{basename}"],  # Argument array
            shell=False,  # <-- SECURITY: Shell interpretation disabled
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return result.stdout.strip()
        
    except subprocess.TimeoutExpired:
        return "error: timeout"
    except Exception as e:
        return f"error: {e}"


# ============================================================
# DEMONSTRATION TESTS
# ============================================================

def test_vulnerable_normal_input():
    """Test vulnerable function with normal input"""
    print("\n=== TEST 1: Vulnerable - Normal Input ===")
    
    normal_filename = "document.txt"
    result = get_file_metadata_vulnerable(normal_filename)
    
    print(f"Input: {normal_filename}")
    print(f"Output: {result}")
    print("Status: No injection detected (expected for normal input)")


def test_vulnerable_command_injection():
    """Test vulnerable function with command injection payload"""
    print("\n=== TEST 2: Vulnerable - Command Injection ===")
    
    # SYNTHETIC HARMLESS PAYLOAD
    # Uses 'echo' markers to demonstrate injection without actual damage
    # In real attack, this could be: filename.txt; rm -rf /;
    malicious_filename = "document.txt; echo INJECTED_COMMAND_EXECUTED"
    
    print(f"Input: {malicious_filename}")
    print("Attempting command injection...")
    
    result = get_file_metadata_vulnerable(malicious_filename)
    
    print(f"Output: {result}")
    
    # Check if injection worked
    if "INJECTED_COMMAND_EXECUTED" in result[0]:
        print("⚠️  COMMAND INJECTION SUCCESSFUL - Vulnerability confirmed!")
    else:
        print("❌ Command injection failed")


def test_vulnerable_pipe_injection():
    """Test vulnerable function with pipe operator"""
    print("\n=== TEST 3: Vulnerable - Pipe Injection ===")
    
    # Pipe operator can chain commands
    malicious_filename = "document.txt | echo PIPE_INJECTION"
    
    print(f"Input: {malicious_filename}")
    result = get_file_metadata_vulnerable(malicious_filename)
    
    print(f"Output: {result}")
    
    if "PIPE_INJECTION" in result[0]:
        print("⚠️  PIPE INJECTION SUCCESSFUL - Vulnerability confirmed!")
    else:
        print("❌ Pipe injection failed")


def test_vulnerable_and_operator():
    """Test vulnerable function with AND operator"""
    print("\n=== TEST 4: Vulnerable - AND Operator ===")
    
    # AND operator executes second command if first succeeds
    malicious_filename = "document.txt && echo AND_INJECTION"
    
    print(f"Input: {malicious_filename}")
    result = get_file_metadata_vulnerable(malicious_filename)
    
    print(f"Output: {result}")
    
    if "AND_INJECTION" in result[0]:
        print("⚠️  AND INJECTION SUCCESSFUL - Vulnerability confirmed!")
    else:
        print("❌ AND injection failed")


def test_secure_normal_input():
    """Test secure function with normal input"""
    print("\n=== TEST 5: Secure - Normal Input ===")
    
    normal_filename = "document.txt"
    result = get_file_metadata_secure(normal_filename)
    
    print(f"Input: {normal_filename}")
    print(f"Output: {result}")
    print("Status: Normal processing works")


def test_secure_rejects_injection():
    """Test secure function rejects command injection"""
    print("\n=== TEST 6: Secure - Rejects Injection ===")
    
    malicious_filename = "document.txt; echo INJECTED"
    
    print(f"Input: {malicious_filename}")
    result = get_file_metadata_secure(malicious_filename)
    
    print(f"Output: {result}")
    
    if "error" in result[0]:
        print("✅ INJECTION REJECTED - Security control working!")
    else:
        print("❌ Injection not rejected")


def test_secure_operation_allowlist():
    """Test secure function validates operation against allow-list"""
    print("\n=== TEST 7: Secure - Operation Allow-list ===")
    
    valid_operation = "analyze"
    invalid_operation = "malicious_operation"
    
    print(f"Valid operation: {valid_operation}")
    result1 = process_file_secure("test.txt", valid_operation)
    print(f"Result: {result1}")
    
    print(f"\nInvalid operation: {invalid_operation}")
    result2 = process_file_secure("test.txt", invalid_operation)
    print(f"Result: {result2}")
    
    if "not allowed" in result2:
        print("✅ Allow-list validation working!")
    else:
        print("❌ Allow-list validation failed")


def test_secure_path_traversal():
    """Test secure function rejects path traversal"""
    print("\n=== TEST 8: Secure - Path Traversal ===")
    
    malicious_path = "../../../etc/passwd"
    
    print(f"Input: {malicious_path}")
    result = process_file_secure(malicious_path, "analyze")
    
    print(f"Output: {result}")
    
    if "invalid path" in result:
        print("✅ Path traversal rejected!")
    else:
        print("❌ Path traversal not rejected")


def test_secure_special_characters():
    """Test secure function rejects special characters"""
    print("\n=== TEST 9: Secure - Special Characters ===")
    
    # Various shell metacharacters
    test_cases = [
        "file`whoami`.txt",      # Backtick substitution
        "file$(whoami).txt",     # Dollar substitution
        "file\ntest.txt",        # Newline
        "file&touch.txt",        # Background
    ]
    
    for test_input in test_cases:
        print(f"\nInput: {test_input}")
        result = get_file_metadata_secure(test_input)
        print(f"Result: {result}")
        
        if "error" in result[0]:
            print("✅ Special characters rejected")
        else:
            print("❌ Special characters not rejected")


# ============================================================
# MAIN DEMONSTRATION
# ============================================================

def main():
    print("=" * 70)
    print("COMMAND INJECTION DEMONSTRATION MODULE")
    print("SecureShare Security Engineering Lab")
    print("=" * 70)
    
    print("\nCWE: CWE-78 (OS Command Injection)")
    print("OWASP: A03:2021 - Injection")
    print("\nSCENARIO: File metadata processor using shell commands")
    print("\nIMPORTANT: All commands use 'echo' for safe demonstration")
    print("          No destructive commands are executed")
    
    print("\n" + "=" * 70)
    print("PART 1: VULNERABLE IMPLEMENTATION TESTS")
    print("=" * 70)
    
    test_vulnerable_normal_input()
    test_vulnerable_command_injection()
    test_vulnerable_pipe_injection()
    test_vulnerable_and_operator()
    
    print("\n" + "=" * 70)
    print("PART 2: SECURE IMPLEMENTATION TESTS")
    print("=" * 70)
    
    test_secure_normal_input()
    test_secure_rejects_injection()
    test_secure_operation_allowlist()
    test_secure_path_traversal()
    test_secure_special_characters()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETED")
    print("=" * 70)
    
    print("\nSUMMARY:")
    print("- Vulnerable version: Accepts and executes shell metacharacters")
    print("- Secure version: Validates input, uses shell=False, argument arrays")
    print("- Security controls: Input validation, allow-listing, path validation")


if __name__ == "__main__":
    main()
