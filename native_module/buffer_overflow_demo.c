/**
 * BUFFER OVERFLOW DEMONSTRATION MODULE
 * 
 * PURPOSE: Educational demonstration of buffer overflow vulnerability
 *          in a filename parsing context (simulating SecureShare functionality)
 * 
 * WARNING: This code contains INTENTIONAL VULNERABILITIES for educational
 *          purposes only. DO NOT use in production or integrate with the
 *          main SecureShare application.
 * 
 * USAGE: Compile with AddressSanitizer to detect the vulnerability:
 *        gcc -fsanitize=address -g -o buffer_overflow_demo buffer_overflow_demo.c
 *        ./buffer_overflow_demo
 * 
 * This file contains BOTH vulnerable and secure implementations for comparison.
 * The vulnerable function will trigger ASAN when called with oversized input.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_FILENAME_LEN 32
#define ORIGINAL_FILENAME_LEN 64

/**
 * VULNERABLE FUNCTION: parse_filename_metadata
 * 
 * This function demonstrates a classic buffer overflow vulnerability.
 * It copies a filename into a fixed-size buffer without bounds checking.
 * 
 * VULNERABILITY: strcpy() does not check destination buffer size.
 * If source string is longer than destination buffer, it will overflow.
 * 
 * MEMORY LAYOUT (stack frame):
 * 
 * High Addresses
 *   ┌─────────────────────────┐
 *   │   saved EBP             │  <- Base pointer of previous frame
 *   ├─────────────────────────┤
 *   │   return address        │  <- Where function will return to
 *   ├─────────────────────────┤
 *   │   metadata_buf[32]      │  <- Buffer for metadata (32 bytes)
 *   │   [0][1]...[31]         │
 *   ├─────────────────────────┤
 *   │   filename_buf[32]      │  <- Buffer for filename (32 bytes)
 *   │   [0][1]...[31]         │  <- OVERFLOW STARTS HERE
 *   ├─────────────────────────┤
 *   │   other local vars      │
 *   └─────────────────────────┘
 * Low Addresses
 * 
 * If we write more than 32 bytes to filename_buf, we overflow into:
 * 1. metadata_buf (corrupting data)
 * 2. saved EBP (corrupting stack frame)
 * 3. return address (potentially hijacking control flow)
 */
void parse_filename_metadata_vulnerable(const char* original_filename) {
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    printf("[VULNERABLE] Parsing filename: %s\n", original_filename);
    printf("[VULNERABLE] Original filename length: %zu\n", strlen(original_filename));
    printf("[VULNERABLE] Destination buffer size: %d\n", MAX_FILENAME_LEN);
    
    // VULNERABLE: No bounds checking on strcpy
    // If original_filename is longer than 32 bytes, this will overflow
    strcpy(filename_buf, original_filename);
    
    // This line may never be reached if overflow corrupts return address
    printf("[VULNERABLE] Parsed filename: %s\n", filename_buf);
    
    // Simulate metadata extraction
    strcpy(metadata_buf, "meta_");
    strcat(metadata_buf, filename_buf);
    
    printf("[VULNERABLE] Metadata: %s\n", metadata_buf);
}

/**
 * SECURE FUNCTION: parse_filename_metadata_secure
 * 
 * This function demonstrates the secure version with proper bounds checking.
 * 
 * SECURITY CONTROLS:
 * 1. Check if source is NULL
 * 2. Check source length against destination size
 * 3. Use strncpy with explicit size limit
 * 4. Ensure null-termination
 * 5. Return error status for caller handling
 * 
 * @param original_filename Input filename
 * @param filename_buf Destination buffer (must be at least MAX_FILENAME_LEN)
 * @param metadata_buf Metadata buffer (must be at least MAX_FILENAME_LEN)
 * @return 0 on success, -1 on error (input too long)
 */
int parse_filename_metadata_secure(const char* original_filename,
                                   char* filename_buf,
                                   char* metadata_buf,
                                   size_t buf_size) {
    // Security Control 1: NULL pointer check
    if (original_filename == NULL || filename_buf == NULL || metadata_buf == NULL) {
        fprintf(stderr, "[SECURE] Error: NULL pointer passed\n");
        return -1;
    }
    
    size_t orig_len = strlen(original_filename);
    
    printf("[SECURE] Parsing filename: %s\n", original_filename);
    printf("[SECURE] Original filename length: %zu\n", orig_len);
    printf("[SECURE] Destination buffer size: %zu\n", buf_size);
    
    // Security Control 2: Bounds check before copy
    if (orig_len >= buf_size) {
        fprintf(stderr, "[SECURE] Error: Input too long (%zu >= %zu)\n", orig_len, buf_size);
        return -1;
    }
    
    // Security Control 3: Safe copy with explicit size limit
    strncpy(filename_buf, original_filename, buf_size - 1);
    
    // Security Control 4: Ensure null-termination
    filename_buf[buf_size - 1] = '\0';
    
    printf("[SECURE] Parsed filename: %s\n", filename_buf);
    
    // Security Control 5: Safe metadata construction with bounds check
    size_t meta_len = strlen("meta_") + orig_len;
    if (meta_len >= buf_size) {
        fprintf(stderr, "[SECURE] Error: Metadata would overflow buffer\n");
        return -1;
    }
    
    strcpy(metadata_buf, "meta_");
    strcat(metadata_buf, filename_buf);
    
    printf("[SECURE] Metadata: %s\n", metadata_buf);
    
    return 0;
}

/**
 * Test case 1: Normal input (should work in both versions)
 */
void test_normal_input() {
    printf("\n=== TEST 1: Normal Input ===\n");
    const char* normal_filename = "document.txt";
    
    printf("\n--- Vulnerable Version ---\n");
    parse_filename_metadata_vulnerable(normal_filename);
    
    printf("\n--- Secure Version ---\n");
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    int result = parse_filename_metadata_secure(normal_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    printf("[SECURE] Result: %s\n", result == 0 ? "SUCCESS" : "FAILED");
}

/**
 * Test case 2: Oversized input (triggers overflow in vulnerable version)
 *
 * This creates a filename that is 64 bytes long, which is double the
 * buffer size of 32 bytes. This will overflow the buffer and corrupt
 * the stack frame.
 *
 * NOTE: This will cause the program to crash or trigger ASAN detection.
 * The test will stop at this point.
 */
void test_oversized_input() {
    printf("\n=== TEST 2: Oversized Input (Buffer Overflow Test) ===\n");

    // Create a 64-byte filename (exactly double the buffer size)
    // This will overflow the 32-byte buffer
    char oversized_filename[ORIGINAL_FILENAME_LEN];
    memset(oversized_filename, 'A', ORIGINAL_FILENAME_LEN - 1);
    oversized_filename[ORIGINAL_FILENAME_LEN - 1] = '\0';

    printf("[TEST] Generated oversized filename length: %zu\n", strlen(oversized_filename));
    printf("[TEST] Filename content (first 40 chars): %.40s...\n", oversized_filename);

    printf("\n--- Vulnerable Version (should trigger ASAN) ---\n");
    printf("[WARNING] This will crash or trigger ASAN detection.\n");
    printf("[WARNING] The program will stop here.\n\n");

    // This will trigger the buffer overflow
    parse_filename_metadata_vulnerable(oversized_filename);

    // This line will likely not be reached
    printf("[ERROR] Should not reach here - overflow did not crash!\n");
}

/**
 * Test case 3: Boundary condition (exactly buffer size)
 */
void test_boundary_input() {
    printf("\n=== TEST 3: Boundary Input (Exactly Buffer Size) ===\n");
    
    // Create a filename that is exactly 32 bytes (buffer size)
    // This is at the boundary - should fail in secure version
    char boundary_filename[MAX_FILENAME_LEN];
    memset(boundary_filename, 'B', MAX_FILENAME_LEN - 1);
    boundary_filename[MAX_FILENAME_LEN - 1] = '\0';
    
    printf("[TEST] Generated boundary filename length: %zu\n", strlen(boundary_filename));
    
    printf("\n--- Vulnerable Version ---\n");
    parse_filename_metadata_vulnerable(boundary_filename);
    
    printf("\n--- Secure Version ---\n");
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    int result = parse_filename_metadata_secure(boundary_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    printf("[SECURE] Result: %s\n", result == 0 ? "SUCCESS" : "FAILED (expected)");
}

/**
 * Test case 4: NULL input (security control test)
 */
void test_null_input() {
    printf("\n=== TEST 4: NULL Input ===\n");
    
    printf("\n--- Vulnerable Version (will crash) ---\n");
    // parse_filename_metadata_vulnerable(NULL);  // Would crash, so we skip
    
    printf("[SKIPPED] Vulnerable version would crash with NULL input\n");
    
    printf("\n--- Secure Version ---\n");
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    int result = parse_filename_metadata_secure(NULL, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    printf("[SECURE] Result: %s (expected)\n", result == -1 ? "FAILED (correctly rejected)" : "SUCCESS");
}

int main() {
    printf("==============================================\n");
    printf("Buffer Overflow Demonstration Module\n");
    printf("SecureShare Security Engineering Lab\n");
    printf("==============================================\n\n");

    printf("IMPORTANT: This demonstration uses AddressSanitizer (ASAN)\n");
    printf("to detect buffer overflows. If compiled with -fsanitize=address,\n");
    printf("the vulnerable version will trigger ASAN detection.\n\n");

    // Run secure tests first (these should all pass)
    printf("=== PART 1: SECURE IMPLEMENTATION TESTS ===\n");
    test_normal_input();
    test_boundary_input();
    test_null_input();

    printf("\n=== PART 2: VULNERABLE IMPLEMENTATION TEST ===\n");
    printf("The following test will trigger a buffer overflow.\n");
    printf("This is expected behavior to demonstrate the vulnerability.\n\n");

    // Run vulnerable test last (will crash)
    test_oversized_input();

    // This line will not be reached due to crash
    printf("\n==============================================\n");
    printf("Demonstration completed.\n");
    printf("==============================================\n");

    return 0;
}
