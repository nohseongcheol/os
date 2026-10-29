#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *தரவு, size_t 바이트수);
ssize_t write(int 파일서술자, const void *தரவு, size_t 바이트수);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t ஆஃப்செட்_மதிப்பு, int திட்டப்பணி_மூலம்);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *கோப்பு_உள்ளீடு_பெயர்);
int ftruncate(int 파일서술자, off_t 바이트수);
int fsync(int 파일서술자);
void _exit(int முடிவு_குறியீடு) __attribute__((noreturn));
#endif
