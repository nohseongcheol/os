#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int fileDescriptor, void *data, size_t byteCount);
ssize_t write(int fileDescriptor, const void *data, size_t byteCount);
int close(int fileDescriptor);
off_t lseek(int fileDescriptor, off_t offsetValue, int projectRoot);
int dup(int fileDescriptor);
int dup2(int fileDescriptor, int newDescriptor);
int unlink(const char *fileEntryName);
int ftruncate(int fileDescriptor, off_t byteCount);
int fsync(int fileDescriptor);
void _exit(int exitCode) __attribute__((noreturn));
#endif
