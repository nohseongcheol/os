#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *ข้อมูล, size_t 바이트수);
ssize_t write(int 파일서술자, const void *ข้อมูล, size_t 바이트수);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t ออฟเซต_ค่า, int แสดง_ราก);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *แฟ้ม_รายการ_ชื่อ);
int ftruncate(int 파일서술자, off_t 바이트수);
int fsync(int 파일서술자);
void _exit(int ออก_รหัส) __attribute__((noreturn));
#endif
