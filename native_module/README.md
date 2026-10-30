# Native Module - Secure File Operations

This directory contains a C/C++ demonstration module showcasing secure file operations and safe programming practices.

## Purpose

This module demonstrates secure C programming techniques that complement the Python Flask application:

- Input validation
- Buffer overflow prevention
- Path traversal protection
- Secure string operations
- File extension whitelisting

## Files

- `secure_file_ops.h` - Header file with function declarations
- `secure_file_ops.c` - Implementation of secure file operations
- `demo.c` - Demonstration program
- `Makefile` - Build configuration

## Building

### Prerequisites

- GCC compiler
- Make utility

### Compile

```bash
make
```

### Run Demo

```bash
make run
```

### Clean

```bash
make clean
```

## Security Features Demonstrated

1. **Filename Validation**
   - Prevents path traversal attacks (`../`)
   - Blocks absolute paths
   - Filters invalid characters

2. **Secure String Operations**
   - Bounds checking on string copies
   - Buffer overflow prevention
   - Safe string handling

3. **Path Sanitization**
   - Removes path traversal sequences
   - Normalizes path separators
   - Prevents directory traversal

4. **File Extension Whitelisting**
   - Case-insensitive comparison
   - Whitelist-based validation
   - Prevents unauthorized file types

5. **Secure File I/O**
   - Bounds checking on reads
   - Safe file operations
   - Error handling

## Integration with Python

This module demonstrates secure programming concepts that can be applied in Python:
- Input validation is done in Python via Flask-WTF
- File operations use Python's secure libraries
- Path handling uses `werkzeug.utils.secure_filename`

## Educational Purpose

This module is for educational purposes to demonstrate:
- The importance of bounds checking in C
- How vulnerabilities like buffer overflows occur
- Secure programming patterns
- Defense-in-depth security
