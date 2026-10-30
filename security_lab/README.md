# Security Lab - Vulnerability Demonstrations

This directory contains isolated demonstrations of security vulnerabilities for educational purposes. These are **NOT** part of the main SecureShare application.

## Purpose

This lab is designed to help students understand:
- Common security vulnerabilities
- How to identify them
- How to fix them
- Defense-in-depth security principles

## Structure

```
security_lab/
├── DISABLED.txt           # Prevents accidental use
├── README.md             # This file
└── C/                    # C vulnerability demonstrations
    ├── unsafe.c          # Vulnerable code examples
    └── safe.c           # Secure alternatives
```

## How to Use

1. **DO NOT** remove DISABLED.txt unless explicitly instructed
2. Study the vulnerable code to understand the vulnerability
3. Compare with the secure implementation
4. Never deploy vulnerable code to production
5. Use only in isolated, controlled environments

## Vulnerabilities Demonstrated

### C Vulnerabilities

1. **Buffer Overflow** - Unsafe string operations
2. **Path Traversal** - Unsanitized file paths
3. **Format String** - Unsafe printf usage
4. **Integer Overflow** - Unsafe arithmetic
5. **Use After Free** - Memory management errors

## Educational Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE (Common Weakness Enumeration): https://cwe.mitre.org/
- Secure Coding Standards: https://wiki.sei.cmu.edu/confluence/display/seccode/SEI+CERT+Coding+Standards

## Disclaimer

This code is for educational purposes only. The vulnerabilities are intentional and should never be used in production. Always follow secure coding practices and perform security reviews before deployment.
