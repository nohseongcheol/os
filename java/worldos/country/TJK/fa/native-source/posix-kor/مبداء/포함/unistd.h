#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *داده_ها, size_t 바이트수);
ssize_t write(int 파일서술자, const void *داده_ها, size_t 바이트수);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t جابجایی_لایه_ای_مقدار, int نمایش_دادن_جذر);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *فایل_ورودی_نام);
int ftruncate(int 파일서술자, off_t 바이트수);
int fsync(int 파일서술자);
void _exit(int خروج_کد) __attribute__((noreturn));
#endif
