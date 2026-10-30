"""
Intentional vulnerability for CI/CD security gate demonstration.

This file contains intentional security issues to demonstrate that the
CI/CD pipeline correctly fails when High/Critical findings are detected.

DO NOT MERGE THIS INTO MAIN/DEVELOP - THIS IS FOR TESTING ONLY.
"""

import os
import subprocess


def vulnerable_eval_usage():
    """Intentionally vulnerable: uses eval() with user input"""
    user_input = "print('pwned')"
    eval(user_input)  # CWE-95: Eval Injection


def hardcoded_secret():
    """Intentionally vulnerable: hardcoded secret"""
    API_KEY = "sk-1234567890abcdef"  # CWE-798: Hardcoded Credentials


def sql_injection():
    """Intentionally vulnerable: SQL injection"""
    user_id = "1 OR 1=1"
    query = f"SELECT * FROM users WHERE id = {user_id}"  # CWE-89: SQL Injection
    return query


if __name__ == "__main__":
    print("This file contains intentional vulnerabilities for CI/CD testing.")
    print("Do not merge this into main or develop branches.")
