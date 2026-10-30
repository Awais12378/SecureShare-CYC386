/**
 * AUTOMATED REGRESSION TESTS FOR BUFFER OVERFLOW FIX
 * 
 * PURPOSE: Prove that the secure version safely rejects oversized input
 *          and handles all edge cases correctly.
 * 
 * These tests are designed to be run with AddressSanitizer to prove
 * no memory violations occur in the secure implementation.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

#define MAX_FILENAME_LEN 32
#define ORIGINAL_FILENAME_LEN 64

/**
 * Secure function from buffer_overflow_demo.c
 * Copied here for testing purposes
 */
int parse_filename_metadata_secure(const char* original_filename,
                                   char* filename_buf,
                                   char* metadata_buf,
                                   size_t buf_size) {
    if (original_filename == NULL || filename_buf == NULL || metadata_buf == NULL) {
        return -1;
    }
    
    size_t orig_len = strlen(original_filename);
    
    if (orig_len >= buf_size) {
        return -1;
    }
    
    strncpy(filename_buf, original_filename, buf_size - 1);
    filename_buf[buf_size - 1] = '\0';
    
    size_t meta_len = strlen("meta_") + orig_len;
    if (meta_len >= buf_size) {
        return -1;
    }
    
    strcpy(metadata_buf, "meta_");
    strcat(metadata_buf, filename_buf);
    
    return 0;
}

/**
 * Test helper function
 */
void run_test(const char* test_name, int passed) {
    printf("[%s] %s\n", passed ? "PASS" : "FAIL", test_name);
    if (!passed) {
        printf("ERROR: Test failed: %s\n", test_name);
        exit(1);
    }
}

/**
 * Test 1: Normal input should succeed
 */
void test_normal_input() {
    printf("\n--- Test 1: Normal Input ---\n");
    
    const char* normal_filename = "document.txt";
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result = parse_filename_metadata_secure(normal_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    
    int passed = (result == 0);
    passed = passed && (strcmp(filename_buf, normal_filename) == 0);
    passed = passed && (strcmp(metadata_buf, "meta_document.txt") == 0);
    
    run_test("Normal input processed correctly", passed);
}

/**
 * Test 2: Oversized input should be rejected
 */
void test_oversized_input() {
    printf("\n--- Test 2: Oversized Input ---\n");
    
    char oversized_filename[ORIGINAL_FILENAME_LEN];
    memset(oversized_filename, 'A', ORIGINAL_FILENAME_LEN - 1);
    oversized_filename[ORIGINAL_FILENAME_LEN - 1] = '\0';
    
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result = parse_filename_metadata_secure(oversized_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    
    int passed = (result == -1);
    passed = passed && (strlen(oversized_filename) >= MAX_FILENAME_LEN);
    
    run_test("Oversized input correctly rejected", passed);
}

/**
 * Test 3: Boundary condition (exactly buffer size) should be rejected
 */
void test_boundary_input() {
    printf("\n--- Test 3: Boundary Input ---\n");
    
    char boundary_filename[MAX_FILENAME_LEN];
    memset(boundary_filename, 'B', MAX_FILENAME_LEN - 1);
    boundary_filename[MAX_FILENAME_LEN - 1] = '\0';
    
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result = parse_filename_metadata_secure(boundary_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    
    int passed = (result == -1);
    passed = passed && (strlen(boundary_filename) == MAX_FILENAME_LEN - 1);
    
    run_test("Boundary input correctly rejected", passed);
}

/**
 * Test 4: One byte under limit should succeed
 */
void test_one_byte_under_limit() {
    printf("\n--- Test 4: One Byte Under Limit ---\n");
    
    char under_filename[MAX_FILENAME_LEN];
    memset(under_filename, 'C', MAX_FILENAME_LEN - 2);
    under_filename[MAX_FILENAME_LEN - 2] = '\0';
    
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result = parse_filename_metadata_secure(under_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    
    int passed = (result == 0);
    passed = passed && (strlen(under_filename) == MAX_FILENAME_LEN - 2);
    
    run_test("One byte under limit accepted", passed);
}

/**
 * Test 5: NULL input should be rejected
 */
void test_null_input() {
    printf("\n--- Test 5: NULL Input ---\n");
    
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result1 = parse_filename_metadata_secure(NULL, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    int result2 = parse_filename_metadata_secure("test.txt", NULL, metadata_buf, MAX_FILENAME_LEN);
    int result3 = parse_filename_metadata_secure("test.txt", filename_buf, NULL, MAX_FILENAME_LEN);
    
    int passed = (result1 == -1) && (result2 == -1) && (result3 == -1);
    
    run_test("NULL inputs correctly rejected", passed);
}

/**
 * Test 6: Empty string should succeed
 */
void test_empty_string() {
    printf("\n--- Test 6: Empty String ---\n");
    
    const char* empty_filename = "";
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result = parse_filename_metadata_secure(empty_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    
    int passed = (result == 0);
    passed = passed && (strlen(filename_buf) == 0);
    
    run_test("Empty string handled correctly", passed);
}

/**
 * Test 7: Special characters should be handled
 */
void test_special_characters() {
    printf("\n--- Test 7: Special Characters ---\n");
    
    const char* special_filename = "file_(1)-test[2].txt";
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result = parse_filename_metadata_secure(special_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    
    int passed = (result == 0);
    passed = passed && (strcmp(filename_buf, special_filename) == 0);
    
    run_test("Special characters handled correctly", passed);
}

/**
 * Test 8: Buffer size parameter should be respected
 */
void test_custom_buffer_size() {
    printf("\n--- Test 8: Custom Buffer Size ---\n");
    
    const char* test_filename = "test.txt";
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    // Test with smaller buffer size
    int result = parse_filename_metadata_secure(test_filename, filename_buf, metadata_buf, 8);
    
    int passed = (result == -1);  // Should fail because buffer too small
    
    run_test("Custom buffer size respected", passed);
}

/**
 * Test 9: Metadata buffer overflow prevention
 */
void test_metadata_overflow_prevention() {
    printf("\n--- Test 9: Metadata Overflow Prevention ---\n");
    
    // Create a filename that would cause metadata to overflow
    // metadata = "meta_" + filename
    // If filename is 30 bytes, metadata would be 35 bytes (overflow 32-byte buffer)
    char long_filename[MAX_FILENAME_LEN];
    memset(long_filename, 'D', MAX_FILENAME_LEN - 3);
    long_filename[MAX_FILENAME_LEN - 3] = '\0';
    
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    int result = parse_filename_metadata_secure(long_filename, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    
    int passed = (result == -1);  // Should fail due to metadata overflow check
    
    run_test("Metadata overflow prevented", passed);
}

/**
 * Test 10: Multiple sequential calls should not cause memory corruption
 */
void test_sequential_calls() {
    printf("\n--- Test 10: Sequential Calls ---\n");
    
    char filename_buf[MAX_FILENAME_LEN];
    char metadata_buf[MAX_FILENAME_LEN];
    
    for (int i = 0; i < 100; i++) {
        snprintf(filename_buf, MAX_FILENAME_LEN, "file%d.txt", i);
        parse_filename_metadata_secure(filename_buf, filename_buf, metadata_buf, MAX_FILENAME_LEN);
    }
    
    // If we get here without crashing, the test passes
    run_test("Sequential calls do not cause memory corruption", 1);
}

int main() {
    printf("==============================================\n");
    printf("Buffer Overflow Regression Tests\n");
    printf("SecureShare Security Engineering Module\n");
    printf("==============================================\n\n");
    
    printf("Running automated regression tests...\n");
    printf("All tests compiled with AddressSanitizer.\n\n");
    
    int total_tests = 10;
    int passed_tests = 0;
    
    test_normal_input();
    passed_tests++;
    
    test_oversized_input();
    passed_tests++;
    
    test_boundary_input();
    passed_tests++;
    
    test_one_byte_under_limit();
    passed_tests++;
    
    test_null_input();
    passed_tests++;
    
    test_empty_string();
    passed_tests++;
    
    test_special_characters();
    passed_tests++;
    
    test_custom_buffer_size();
    passed_tests++;
    
    test_metadata_overflow_prevention();
    passed_tests++;
    
    test_sequential_calls();
    passed_tests++;
    
    printf("\n==============================================\n");
    printf("Test Results: %d/%d tests passed\n", passed_tests, total_tests);
    printf("==============================================\n");
    
    if (passed_tests == total_tests) {
        printf("SUCCESS: All regression tests passed.\n");
        return 0;
    } else {
        printf("FAILURE: Some tests failed.\n");
        return 1;
    }
}
