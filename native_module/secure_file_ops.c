#include "secure_file_ops.h"
#include <ctype.h>

bool validate_filename(const char* filename) {
    if (filename == NULL || strlen(filename) == 0 || strlen(filename) >= MAX_FILENAME_LEN) {
        return false;
    }
    
    // Check for path traversal attempts
    if (strstr(filename, "..") != NULL) {
        return false;
    }
    
    // Check for absolute path
    if (filename[0] == '/' || filename[0] == '\\') {
        return false;
    }
    
    // Check for invalid characters
    const char* invalid_chars = "<>:\"/\\|?*";
    for (size_t i = 0; i < strlen(filename); i++) {
        if (strchr(invalid_chars, filename[i]) != NULL) {
            return false;
        }
    }
    
    return true;
}

int secure_file_read(const char* filepath, char* buffer, size_t buffer_size) {
    if (filepath == NULL || buffer == NULL || buffer_size == 0) {
        return -1;
    }
    
    FILE* file = fopen(filepath, "rb");
    if (file == NULL) {
        return -1;
    }
    
    size_t bytes_read = 0;
    size_t chunk;
    
    while (bytes_read < buffer_size - 1) {
        chunk = fread(buffer + bytes_read, 1, BUFFER_SIZE, file);
        if (chunk == 0) {
            break;
        }
        bytes_read += chunk;
    }
    
    fclose(file);
    buffer[bytes_read] = '\0';
    
    return (int)bytes_read;
}

int secure_file_write(const char* filepath, const char* content, size_t content_size) {
    if (filepath == NULL || content == NULL || content_size == 0) {
        return -1;
    }
    
    FILE* file = fopen(filepath, "wb");
    if (file == NULL) {
        return -1;
    }
    
    size_t bytes_written = fwrite(content, 1, content_size, file);
    
    fclose(file);
    
    return (int)bytes_written;
}

bool secure_strcpy(char* dest, const char* src, size_t dest_size) {
    if (dest == NULL || src == NULL || dest_size == 0) {
        return false;
    }
    
    size_t src_len = strlen(src);
    if (src_len >= dest_size) {
        // Truncate to fit
        strncpy(dest, src, dest_size - 1);
        dest[dest_size - 1] = '\0';
        return false;
    }
    
    strcpy(dest, src);
    return true;
}

bool sanitize_path(const char* path, char* sanitized, size_t sanitized_size) {
    if (path == NULL || sanitized == NULL || sanitized_size == 0) {
        return false;
    }
    
    size_t path_len = strlen(path);
    size_t j = 0;
    
    for (size_t i = 0; i < path_len && j < sanitized_size - 1; i++) {
        // Remove path traversal sequences
        if (i < path_len - 1 && path[i] == '.' && path[i + 1] == '.') {
            i++; // Skip the second dot
            continue;
        }
        
        // Replace backslashes with forward slashes
        if (path[i] == '\\') {
            sanitized[j++] = '/';
            continue;
        }
        
        sanitized[j++] = path[i];
    }
    
    sanitized[j] = '\0';
    return true;
}

bool check_file_extension(const char* filename, const char** allowed_extensions, int num_extensions) {
    if (filename == NULL || allowed_extensions == NULL || num_extensions == 0) {
        return false;
    }
    
    // Find the last dot in filename
    const char* dot = strrchr(filename, '.');
    if (dot == NULL || dot == filename) {
        return false; // No extension or dot at start
    }
    
    const char* extension = dot + 1;
    
    // Convert to lowercase for comparison
    char ext_lower[32];
    size_t i = 0;
    while (extension[i] != '\0' && i < sizeof(ext_lower) - 1) {
        ext_lower[i] = tolower(extension[i]);
        i++;
    }
    ext_lower[i] = '\0';
    
    // Check against whitelist
    for (int j = 0; j < num_extensions; j++) {
        if (allowed_extensions[j] != NULL) {
            char allowed_lower[32];
            size_t k = 0;
            while (allowed_extensions[j][k] != '\0' && k < sizeof(allowed_lower) - 1) {
                allowed_lower[k] = tolower(allowed_extensions[j][k]);
                k++;
            }
            allowed_lower[k] = '\0';
            
            if (strcmp(ext_lower, allowed_lower) == 0) {
                return true;
            }
        }
    }
    
    return false;
}
