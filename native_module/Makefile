# Makefile for Buffer Overflow Demonstration
# SecureShare Security Engineering Module

CC = gcc
CFLAGS = -Wall -Wextra -g
ASAN_FLAGS = -fsanitize=address -fno-omit-frame-pointer
STACK_PROT_FLAGS = -fstack-protector-strong

# Source files
VULN_SRC = buffer_overflow_demo.c
SECURE_SRC = buffer_overflow_demo.c
TEST_SRC = buffer_overflow_test.c

# Output executables
VULN_BIN = buffer_overflow_vulnerable
SECURE_BIN = buffer_overflow_secure
TEST_BIN = buffer_overflow_test

# Default target
all: $(VULN_BIN) $(SECURE_BIN) $(TEST_BIN)

# Compile vulnerable version with ASAN
# Note: The vulnerable function is in the same file as secure function
# We compile it to demonstrate ASAN detection
$(VULN_BIN): $(VULN_SRC)
	$(CC) $(CFLAGS) $(ASAN_FLAGS) $(VULN_SRC) -o $(VULN_BIN)
	@echo "Built demonstration version with AddressSanitizer: $(VULN_BIN)"

# Compile secure version with ASAN and stack protection
$(SECURE_BIN): $(SECURE_SRC)
	$(CC) $(CFLAGS) $(ASAN_FLAGS) $(STACK_PROT_FLAGS) $(SECURE_SRC) -o $(SECURE_BIN)
	@echo "Built secure version with ASAN and stack protection: $(SECURE_BIN)"

# Compile test binary
$(TEST_BIN): $(TEST_SRC)
	$(CC) $(CFLAGS) $(ASAN_FLAGS) $(STACK_PROT_FLAGS) $(TEST_SRC) -o $(TEST_BIN)
	@echo "Built test binary: $(TEST_BIN)"

# Run vulnerable version (should trigger ASAN)
run-vuln: $(VULN_BIN)
	@echo "Running vulnerable version..."
	@./$(VULN_BIN) 2>&1 | tee asan_output_vulnerable.log
	@echo "Output saved to asan_output_vulnerable.log"

# Run secure version (should NOT trigger ASAN)
run-secure: $(SECURE_BIN)
	@echo "Running secure version..."
	@./$(SECURE_BIN) 2>&1 | tee asan_output_secure.log
	@echo "Output saved to asan_output_secure.log"

# Run automated tests
run-tests: $(TEST_BIN)
	@echo "Running automated tests..."
	@./$(TEST_BIN) 2>&1 | tee test_output.log
	@echo "Test output saved to test_output.log"

# Clean build artifacts
clean:
	rm -f $(VULN_BIN) $(SECURE_BIN) $(TEST_BIN)
	rm -f *.log
	rm -f asan_output_*.log test_output.log
	@echo "Cleaned build artifacts"

# Check for ASAN support
check-asan:
	@echo "Checking for AddressSanitizer support..."
	@$(CC) --version
	@echo "ASAN is supported if you have GCC 4.8+ or Clang 3.1+"

.PHONY: all run-vuln run-secure run-tests clean check-asan
