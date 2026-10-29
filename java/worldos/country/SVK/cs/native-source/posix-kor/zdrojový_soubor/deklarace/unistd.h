#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int Soubor_popisovač, void *data, size_t bajt_POČET);
ssize_t write(int Soubor_popisovač, const void *data, size_t bajt_POČET);
int close(int Soubor_popisovač);
off_t lseek(int Soubor_popisovač, off_t POSUN_HODNOTA, int akce_kořen);
int dup(int Soubor_popisovač);
int dup2(int Soubor_popisovač, int 새서술자);
int unlink(const char *Soubor_položka_název);
int ftruncate(int Soubor_popisovač, off_t bajt_POČET);
int fsync(int Soubor_popisovač);
void _exit(int ukončovací_kód) __attribute__((noreturn));
#endif
