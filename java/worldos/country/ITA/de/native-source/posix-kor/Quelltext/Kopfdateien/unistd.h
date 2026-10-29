#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int dateiDeskriptor, void *Daten, size_t byteAnzahl);
ssize_t write(int dateiDeskriptor, const void *Daten, size_t byteAnzahl);
int close(int dateiDeskriptor);
off_t lseek(int dateiDeskriptor, off_t versatzwertWert, int projektWurzel);
int dup(int dateiDeskriptor);
int dup2(int dateiDeskriptor, int neuDeskriptor);
int unlink(const char *dateiEintragName);
int ftruncate(int dateiDeskriptor, off_t byteAnzahl);
int fsync(int dateiDeskriptor);
void _exit(int verlassenProzessKode) __attribute__((noreturn));
#endif
