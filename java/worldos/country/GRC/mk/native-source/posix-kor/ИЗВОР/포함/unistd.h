#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *податоци, size_t бајт_COUNT);
ssize_t write(int 파일서술자, const void *податоци, size_t бајт_COUNT);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_корен);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *датотека_внес_име);
int ftruncate(int 파일서술자, off_t бајт_COUNT);
int fsync(int 파일서술자);
void _exit(int Излез_CODE) __attribute__((noreturn));
#endif
