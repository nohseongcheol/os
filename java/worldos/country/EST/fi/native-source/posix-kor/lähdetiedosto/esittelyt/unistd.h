#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *data, size_t tavu_LASKE);
ssize_t write(int 파일서술자, const void *data, size_t tavu_LASKE);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t SIIRTYMÄ_ARVO, int aloite_juuri);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *Tiedosto_merkintä_nimi);
int ftruncate(int 파일서술자, off_t tavu_LASKE);
int fsync(int 파일서술자);
void _exit(int lopetuskoodi) __attribute__((noreturn));
#endif
