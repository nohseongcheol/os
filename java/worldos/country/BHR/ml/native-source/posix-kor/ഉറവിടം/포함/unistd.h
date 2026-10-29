#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *ഡാറ്റാ, size_t 바이트수);
ssize_t write(int 파일서술자, const void *ഡാറ്റാ, size_t 바이트수);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t ഓഫ്_സെറ്റ്_മൂല്യം, int പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *ഫയല്_എന്_ട്രി_നാ_മം);
int ftruncate(int 파일서술자, off_t 바이트수);
int fsync(int 파일서술자);
void _exit(int പുറത്തുകടക്കൽ_കോഡ്) __attribute__((noreturn));
#endif
