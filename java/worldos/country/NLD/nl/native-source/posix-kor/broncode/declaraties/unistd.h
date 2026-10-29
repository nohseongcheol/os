#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *gegevens, size_t byte_AANTAL);
ssize_t write(int 파일서술자, const void *gegevens, size_t byte_AANTAL);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t VERSCHUIVING_WAARDE, int Taken_wortel);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *Bestand_invoer_naam);
int ftruncate(int 파일서술자, off_t byte_AANTAL);
int fsync(int 파일서술자);
void _exit(int afsluitcode) __attribute__((noreturn));
#endif
