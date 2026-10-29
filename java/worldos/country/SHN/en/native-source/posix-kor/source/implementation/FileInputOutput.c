#include <FileABI.h>
#include "CallBoundary.h"

int errorNumber;
int invocationResult(int result) {
    if (result < 0) { errorNumber = -result; return -1; }
    return result;
}
int open(const char *fileEntryName, int openSettings, ...) {
    mode_t grantPermission = 0;
    if (openSettings & O_CREAT) {
        __builtin_va_list arguments;
        __builtin_va_start(arguments, openSettings);
        grantPermission = __builtin_va_arg(arguments, mode_t);
        __builtin_va_end(arguments);
    }
    return invocationResult(jkoros_syscall(30, (int)fileEntryName, openSettings, grantPermission, 0, 0));
}
int creat(const char *fileEntryName, mode_t grantPermission) { return open(fileEntryName, O_WRONLY | O_CREAT | O_TRUNC, grantPermission); }
ssize_t read(int fileDescriptor, void *data, size_t byteCount) {
    return invocationResult(jkoros_syscall(31, fileDescriptor, (int)data, byteCount, 0, 0));
}
ssize_t write(int fileDescriptor, const void *data, size_t byteCount) {
    return invocationResult(jkoros_syscall(32, fileDescriptor, (int)data, byteCount, 0, 0));
}
int close(int fileDescriptor) { return invocationResult(jkoros_syscall(33, fileDescriptor, 0, 0, 0, 0)); }
off_t lseek(int fileDescriptor, off_t offsetValue, int projectRoot) {
    return invocationResult(jkoros_syscall(34, fileDescriptor, offsetValue, projectRoot, 0, 0));
}
int dup(int fileDescriptor) { return invocationResult(jkoros_syscall(35, fileDescriptor, 0, 0, 0, 0)); }
int dup2(int fileDescriptor, int newDescriptor) { return invocationResult(jkoros_syscall(36, fileDescriptor, newDescriptor, 0, 0, 0)); }
int fstat(int fileDescriptor, struct stat *stateValue) { return invocationResult(jkoros_syscall(37, fileDescriptor, (int)stateValue, 0, 0, 0)); }
int unlink(const char *fileEntryName) { return invocationResult(jkoros_syscall(38, (int)fileEntryName, 0, 0, 0, 0)); }
int ftruncate(int fileDescriptor, off_t byteCount) { return invocationResult(jkoros_syscall(39, fileDescriptor, byteCount, 0, 0, 0)); }
int fsync(int fileDescriptor) { return invocationResult(jkoros_syscall(47, fileDescriptor, 0, 0, 0, 0)); }
int fcntl(int fileDescriptor, int command, ...) {
    int value = 0;
    if (command == F_DUPFD || command == F_DUPFD_CLOEXEC || command == F_SETFD || command == F_SETFL) {
        __builtin_va_list arguments;
        __builtin_va_start(arguments, command); value = __builtin_va_arg(arguments, int); __builtin_va_end(arguments);
    }
    return invocationResult(jkoros_syscall(40, fileDescriptor, command, value, 0, 0));
}
