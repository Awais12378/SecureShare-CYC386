#include "secure_file_ops.h"
#include <stdio.h>

void test_validate_filename() {
    printf("Testing validate_filename():\n");
    
    printf("  'test.txt': %s\n", validate_filename("test.txt") ? "PASS" : "FAIL");
    printf("  '../etc/passwd': %s\n", validate_filename("../etc/passwd") ? "FAIL (expected)" : "PASS");
    printf("  '/absolute/path': %s\n", validate_filename("/absolute/path") ? "FAIL (expected)" : "PASS");
    printf("  'file<name>.txt': %s\n", validate_filename("file<name>.txt") ? "FAIL (expected)" : "PASS");
    printf("  'normal_file.pdf': %s\n", validate_filename("normal_file.pdf") ? "PASS" : "FAIL");
    printf("\n");
}

void test_secure_strcpy() {
    printf("Testing secure_strcpy():\n");
    
    char dest1[20];
    bool result1 = secure_strcpy(dest1, "Hello", sizeof(dest1));
    printf("  Copy 'Hello': %s (result: %s)\n", dest1, result1 ? "PASS" : "FAIL");
    
    char dest2[10];
    bool result2 = secure_strcpy(dest2, "This is too long", sizeof(dest2));
    printf("  Copy long string: '%s' (truncated: %s)\n", dest2, result2 ? "FAIL" : "PASS");
    printf("\n");
}

void test_sanitize_path() {
    printf("Testing sanitize_path():\n");
    
    char sanitized1[MAX_PATH_LEN];
    bool result1 = sanitize_path("normal/path/file.txt", sanitized1, sizeof(sanitized1));
    printf("  'normal/path/file.txt': '%s' (result: %s)\n", sanitized1, result1 ? "PASS" : "FAIL");
    
    char sanitized2[MAX_PATH_LEN];
    bool result2 = sanitize_path("../secret/file.txt", sanitized2, sizeof(sanitized2));
    printf("  '../secret/file.txt': '%s' (result: %s)\n", sanitized2, result2 ? "PASS" : "FAIL");
    
    char sanitized3[MAX_PATH_LEN];
    bool result3 = sanitize_path("path\\to\\file.txt", sanitized3, sizeof(sanitized3));
    printf("  'path\\to\\file.txt': '%s' (result: %s)\n", sanitized3, result3 ? "PASS" : "FAIL");
    printf("\n");
}

void test_check_file_extension() {
    printf("Testing check_file_extension():\n");
    
    const char* allowed[] = {"txt", "pdf", "png", "jpg"};
    int num_allowed = 4;
    
    printf("  Allowed: txt, pdf, png, jpg\n");
    printf("  'document.txt': %s\n", check_file_extension("document.txt", allowed, num_allowed) ? "PASS" : "FAIL");
    printf("  'image.png': %s\n", check_file_extension("image.png", allowed, num_allowed) ? "PASS" : "FAIL");
    printf("  'malware.exe': %s\n", check_file_extension("malware.exe", allowed, num_allowed) ? "FAIL (expected)" : "PASS");
    printf("  'FILE.PDF': %s\n", check_file_extension("FILE.PDF", allowed, num_allowed) ? "PASS" : "FAIL");
    printf("\n");
}

void test_secure_file_operations() {
    printf("Testing secure file operations:\n");
    
    const char* test_file = "test_secure_file.txt";
    const char* test_content = "This is a test file for secure file operations.";
    
    // Write test
    int written = secure_file_write(test_file, test_content, strlen(test_content));
    printf("  Write %d bytes: %s\n", written, written > 0 ? "PASS" : "FAIL");
    
    // Read test
    char buffer[256];
    int read = secure_file_read(test_file, buffer, sizeof(buffer));
    printf("  Read %d bytes: %s\n", read, read > 0 ? "PASS" : "FAIL");
    printf("  Content matches: %s\n", strcmp(buffer, test_content) == 0 ? "PASS" : "FAIL");
    
    // Cleanup
    remove(test_file);
    printf("\n");
}

int main() {
    printf("========================================\n");
    printf("Secure File Operations Module Demo\n");
    printf("========================================\n\n");
    
    test_validate_filename();
    test_secure_strcpy();
    test_sanitize_path();
    test_check_file_extension();
    test_secure_file_operations();
    
    printf("========================================\n");
    printf("Demo completed.\n");
    printf("========================================\n");
    
    return 0;
}
