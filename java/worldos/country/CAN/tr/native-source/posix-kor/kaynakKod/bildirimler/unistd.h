#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int Dosya_tanımlayıcı, void *veri, size_t bayt_BAĞ_DEĞ_SAY);
ssize_t write(int Dosya_tanımlayıcı, const void *veri, size_t bayt_BAĞ_DEĞ_SAY);
int close(int Dosya_tanımlayıcı);
off_t lseek(int Dosya_tanımlayıcı, off_t Ofset_değer, int işlem_kök);
int dup(int Dosya_tanımlayıcı);
int dup2(int Dosya_tanımlayıcı, int 새서술자);
int unlink(const char *Dosya_girdi_ad);
int ftruncate(int Dosya_tanımlayıcı, off_t bayt_BAĞ_DEĞ_SAY);
int fsync(int Dosya_tanımlayıcı);
void _exit(int çıkış_kodu) __attribute__((noreturn));
#endif
