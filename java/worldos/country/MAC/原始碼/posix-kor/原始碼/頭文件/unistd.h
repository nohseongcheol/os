#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 檔案描述符, void *資料, size_t 位元組個數);
ssize_t write(int 檔案描述符, const void *資料, size_t 位元組個數);
int close(int 檔案描述符);
off_t lseek(int 檔案描述符, off_t 偏移值, int 項目根);
int dup(int 檔案描述符);
int dup2(int 檔案描述符, int 新建描述符);
int unlink(const char *檔案條目名稱);
int ftruncate(int 檔案描述符, off_t 位元組個數);
int fsync(int 檔案描述符);
void _exit(int 退出程式碼) __attribute__((noreturn));
#endif
