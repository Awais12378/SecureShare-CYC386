#ifndef SECURE_FILE_OPS_H
#define SECURE_FILE_OPS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_FILENAME_LEN 256
#define MAX_PATH_LEN 512
#define BUFFER_SIZE 4096

/**
 * Secure file operations module for SecureShare
 * Demonstrates secure C programming practices
 */

/**
 * Validate filename for security
 * Prevents path traversal and ensures safe filenames
 * 
 * @param filename The filename to validate
 * @return true if filename is safe, false otherwise
 */
bool validate_filename(const char* filename);

/**
 * Secure file read with bounds checking
 * Reads file content safely with buffer overflow protection
 * 
 * @param filepath Path to the file
 * @param buffer Buffer to store content
 * @param buffer_size Size of the buffer
 * @return Number of bytes read, or -1 on error
 */
int secure_file_read(const char* filepath, char* buffer, size_t buffer_size);

/**
 * Secure file write with bounds checking
 * Writes content to file safely
 * 
 * @param filepath Path to the file
 * @param content Content to write
 * @param content_size Size of content
 * @return Number of bytes written, or -1 on error
 */
int secure_file_write(const char* filepath, const char* content, size_t content_size);

/**
 * Secure string copy with length checking
 * Prevents buffer overflow vulnerabilities
 * 
 * @param dest Destination buffer
 * @param src Source string
 * @param dest_size Size of destination buffer
 * @return true if copy succeeded, false if truncated
 */
bool secure_strcpy(char* dest, const char* src, size_t dest_size);

/**
 * Sanitize path to prevent directory traversal
 * Removes path traversal sequences
 * 
 * @param path The path to sanitize
 * @param sanitized Buffer to store sanitized path
 * @param sanitized_size Size of sanitized buffer
 * @return true if sanitization succeeded
 */
bool sanitize_path(const char* path, char* sanitized, size_t sanitized_size);

/**
 * Check file extension against whitelist
 * 
 * @param filename The filename to check
 * @param allowed_extensions Array of allowed extensions
 * @param num_extensions Number of extensions in array
 * @return true if extension is allowed
 */
bool check_file_extension(const char* filename, const char** allowed_extensions, int num_extensions);

#endif // SECURE_FILE_OPS_H
