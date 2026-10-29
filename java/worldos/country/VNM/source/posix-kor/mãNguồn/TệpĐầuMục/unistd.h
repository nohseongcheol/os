#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int bộMôTảTệp, void *DữLiệu, size_t sốLượngByte);
ssize_t write(int bộMôTảTệp, const void *DữLiệu, size_t sốLượngByte);
int close(int bộMôTảTệp);
off_t lseek(int bộMôTảTệp, off_t giáTrịĐộLệch, int gốcCâyDựÁn);
int dup(int bộMôTảTệp);
int dup2(int bộMôTảTệp, int bộMôTảMới);
int unlink(const char *tênMụcTệp);
int ftruncate(int bộMôTảTệp, off_t sốLượngByte);
int fsync(int bộMôTảTệp);
void _exit(int mãRa) __attribute__((noreturn));
#endif
